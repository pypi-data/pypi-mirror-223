import boto3
import pandas as pd


class DynamodbCrud:

    def __init__(
            self,
            endpoint_url,
            region_name,
            aws_access_key_id,
            aws_secret_access_key
    ):
        self.dynamodb = boto3.resource(
            "dynamodb",
            endpoint_url=endpoint_url,
            region_name=region_name,
            aws_access_key_id=aws_access_key_id,
            aws_secret_access_key=aws_secret_access_key
        )

    def create_entry(self, table_name, content):
        table = self.dynamodb.Table(table_name)
        content_without_key = [{key: value for key, value in issue.items() if key != "key"} for issue in content]

        with table.batch_writer() as batch:
            for index, issue in enumerate(content):
                batch.put_item(
                    Item={"Id": content[index]["key"], **content_without_key[index]}
                )

        print("Successfully inserted data")

    def read_data(self, table_name):
        table = self.dynamodb.Table(table_name)
        scan_response = table.scan(TableName=table_name)["Items"]

        df = pd.DataFrame(scan_response)

        return df

    def update_data(self, table_name, content):
        table = self.dynamodb.Table(table_name)
        for commit_id, commit_hash in content.items():
            table.update_item(
                Key={'Id': commit_id},
                UpdateExpression='SET commit_hash = :val',
                ExpressionAttributeValues={':val': commit_hash}
            )
        print("Successfully updated DB")

    def delete_entry(self):
        pass

