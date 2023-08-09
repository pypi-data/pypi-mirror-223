import io
import pandas as pd
from datetime import datetime
from .GenericWriter import GenericWriter
from ..Types import target_type_is_numeric
from ..Contracts.WriterInterface import WriterInterface
from ..Services.AdapterSourceTarget import AdapterSourceTarget


class WriterCDC(GenericWriter, WriterInterface):
    def create_statement_delete(self, row):
        statement_delete = "1=1"
        for cup in self.struct.columns_upsert:
            for c in self.struct.columns:
                if c["target_name"] == cup:
                    source_name = c["source_name"]
                    target_name = c["target_name"]
                    target_type = c["target_type"]

            if target_type_is_numeric(target_type):
                statement_delete = (
                    f'{statement_delete} and "{target_name}" = {row[source_name]}'
                )
            else:
                statement_delete = (
                    f"{statement_delete} and \"{target_name}\" = '{row[source_name]}'"
                )

        return f"({statement_delete})"

    def get_deleted_rows(self, df):
        df = df[df["Op"] == "D"]
        df = df[self.struct.columns_upsert]
        return df

    def delete_data(self, df):
        df = self.get_deleted_rows(df)
        delete_statement = "1!=1"
        for index, row in df.iterrows():
            delete_statement = (
                f"{delete_statement} or {self.create_statement_delete(row)}"
            )

        if delete_statement != "1!=1":
            delete_statement = f"""
                DELETE FROM {self.target_relation}
                WHERE {delete_statement};
            """

            self.target_cursor.execute(delete_statement)

            self.migrator_redshift_connector.target_conn.commit()

    def get_upsert_rows(self, df, op="I"):
        df = df[df["Op"] == op]
        df = df.drop(columns=["Op"])
        return df

    def save_upsert_data_on_tmp_s3(self, bucket, df, path_file, file_name):
        def save_data_on_tmp(op, df, path_file):
            df = self.get_upsert_rows(df, op=op)
            adapter = AdapterSourceTarget(self.struct)
            df = adapter.convert_types(df)
            df = adapter.transform_data(df)
            df = adapter.equalize_number_columns(df)

            if df.empty is False:
                buffer = io.BytesIO()
                df.to_csv(buffer, index=False)
                self.migrator_redshift_connector.s3_session.Object(
                    bucket,
                    path_file,
                ).put(Body=buffer.getvalue())
                buffer.close()

        save_data_on_tmp("I", df, f"{path_file}/insert/{file_name}")
        save_data_on_tmp("U", df, f"{path_file}/update/{file_name}")

    def check_s3_path_exists(self, bucket, key):
        if bucket is None:
            return False

        bucket_client = self.migrator_redshift_connector.s3_session.Bucket(bucket)
        for object_summary in bucket_client.objects.filter(Prefix=key):
            return True
        return False

    def save_to_redshift_from_s3(self, path_file, bucket):
        if self.check_s3_path_exists(bucket, path_file) is True:
            self.create_table_temp_target_relation()
            self.copy_data_to_target(
                f"s3://{bucket}/{path_file}", self.temp_target_relation
            )
            self.migrator_redshift_connector.target_conn.commit()

            self.delete_upsert_data_from_target()
            self.insert_data_from_temp_to_target()

            self.migrator_redshift_connector.target_conn.commit()

            self.drop_table_temp_target_relation()

            self.migrator_redshift_connector.target_conn.commit()

    def delete_on_tmp_s3(self, bucket, path_file):
        if self.check_s3_path_exists(bucket, path_file) is True:
            bucket_client = self.migrator_redshift_connector.s3_session.Bucket(bucket)
            bucket_client.objects.filter(Prefix=f"{path_file}/insert/").delete()
            bucket_client.objects.filter(Prefix=f"{path_file}/update/").delete()

    def save_data(self, operations):
        self.migrator_redshift_connector.connect_s3()
        time = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
        path_file = f"raw/tmp/{self.env}/{self.struct.target_schema}/{self.struct.target_table}/{time}"
        bucket = None

        try:
            for operation in operations:
                url = operation.url

                splitted_url = url.split("/")
                bucket = splitted_url[2]
                key = "/".join(splitted_url[3:])
                file_name = key.split("/")[-1]
                file_name = file_name.replace(".parquet", ".csv")

                obj = self.migrator_redshift_connector.s3_session.Object(bucket, key)
                file_content = obj.get()["Body"].read()

                df = pd.read_parquet(io.BytesIO(file_content))

                self.delete_data(df)
                self.save_upsert_data_on_tmp_s3(bucket, df, path_file, file_name)

            self.save_to_redshift_from_s3(f"{path_file}/insert/", bucket)
            self.save_to_redshift_from_s3(f"{path_file}/update/", bucket)

            self.delete_on_tmp_s3(bucket, path_file)
        except Exception as e:
            if bucket is not None:
                self.delete_on_tmp_s3(bucket, path_file)
            raise e
