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

## S3 Policy Document for Storage Bucket - GetObject
data "aws_iam_policy_document" "lambda_get_policy_doc" {
    statement {
      effect = "Allow"
      actions = [
        "s3:GetObject"
      ]
      resources = ["${aws_s3_bucket.storage_bucket.arn}"]
    }
}

## S3 Policy for Storage Bucket
resource "aws_iam_policy" "lambda_get_policy" {
    name_prefix = "lambda-get-"
    policy = data.aws_iam_policy_document.lambda_get_policy_doc.json

}

## S3 Get Attachment
resource "aws_iam_role_policy_attachment" "lambda_s3_get_attachment" {
    role = aws_iam_role.role_for_lambda.name
    policy_arn = resource.aws_iam_policy.lambda_get_policy.arn
}

## S3 Policy Document for Target Bucket - PutObject
data "aws_iam_policy_document" "lambda_put_policy_doc" {
    statement {
      effect = "Allow"
      actions = [
        "s3:PutObject"
      ]
      resources = ["${aws_s3_bucket.target_bucket.arn}"]
    }
}

## S3 Policy for Target Bucket
resource "aws_iam_policy" "lambda_put_policy" {
    name_prefix = "lambda-put-"
    policy = data.aws_iam_policy_document.lambda_put_policy_doc.json

}

## S3 Put Attachment
resource "aws_iam_role_policy_attachment" "lambda_s3_put_attachment" {
    role = aws_iam_role.role_for_lambda.name
    policy_arn = resource.aws_iam_policy.lambda_put_policy.arn
}