import boto3
import json


def process_invoice_with_textract(s3_bucket, file_name):
    """
    AWS Textractを使用して請求書のテキストを抽出する関数。
    S3に保存されたファイルをTextractで解析し、結果を返す。

    :param s3_bucket: S3のバケット名
    :param file_name: S3内のファイル名
    :return: OCRで抽出した請求書のテキストデータ
    """
    client = boto3.client("textract", region_name="ap-northeast-1")

    response = client.analyze_document(
        Document={"S3Object": {"Bucket": s3_bucket, "Name": file_name}},
        FeatureTypes=["FORMS"],
    )

    extracted_text = []
    for block in response["Blocks"]:
        if block["BlockType"] == "LINE":
            extracted_text.append(block["Text"])

    return "\n".join(extracted_text)
