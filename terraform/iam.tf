## Role Assumption
data "aws_iam_policy_document" "assume_role" {
    statement {
        effect = "Allow"
        
        principals {
          type = "Service"
          identifiers = ["lambda.amazonaws.com"]
        }

    actions = ["sts:AssumeRole"]
    }  
}

## Role
resource "aws_iam_role" "role_for_lambda" {
    name = "role_for_lambda"
    assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

## S3 Policy Document
data "aws_iam_policy_document" "lambda_policy_doc" {
    statement {
      effect = "Allow"
      actions = [
        "s3:GetObject"
      ]
      resources = ["${aws_s3_bucket.storage_bucket.arn}"]
    }
}

## S3 Policy
resource "aws_iam_policy" "lambda_policy" {
    name_prefix = "lambda"
    policy = data.aws_iam_policy_document.lambda_policy_doc.json

}

## S3 Attachment
resource "aws_iam_role_policy_attachment" "lambda_s3_get_attachment" {
    role = aws_iam_role.role_for_lambda.name
    policy_arn = resource.aws_iam_policy.lambda_policy.arn
}