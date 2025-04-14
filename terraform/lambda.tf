## Archive file for Python Lambda Handler Function
data "archive_file" "lambda_code" {
    type = "zip"
    source_file = "${path.module}/../src/lambda_func.py"
    output_path = "compressed_lambda_file.zip"
}

## Lambda Function
resource "aws_lambda_function" "lambda_func" {
    filename = "compressed_lambda_file.zip"
    function_name = "lambda_func"
    role = aws_iam_role.role_for_lambda.arn
    handler = "lambda_func.lambda_handler"
    timeout = 30
    source_code_hash = data.archive_file.lambda_code.output_base64sha256
    runtime = "python3.12"
    layers = ["arn:aws:lambda:eu-west-2:336392948345:layer:AWSSDKPandas-Python312:14"]
}
