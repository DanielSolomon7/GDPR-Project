## Assume Role for Lambda
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

## Role for Lambda
resource "aws_iam_role" "role_for_lambda" {
    name = "role_for_lambda"
    assume_role_policy = data.aws_iam_policy_document.assume_role.json
}

## GetObject permission from Storage Bucket for Lambda
data "aws_iam_policy_document" "lambda_get_policy_doc" {
    statement {
      effect = "Allow"
      actions = [
        "s3:GetObject",
        "s3:ListBucket"
      ]
      resources = ["${aws_s3_bucket.storage_bucket.arn}",
                  "${aws_s3_bucket.storage_bucket.arn}/*"]
    }
}

## Policy for GetObject permission
resource "aws_iam_policy" "lambda_get_policy" {
    name_prefix = "lambda-get-"
    policy = data.aws_iam_policy_document.lambda_get_policy_doc.json

}

## Attachment for GetObject permission
resource "aws_iam_role_policy_attachment" "lambda_s3_get_attachment" {
    role = aws_iam_role.role_for_lambda.name
    policy_arn = resource.aws_iam_policy.lambda_get_policy.arn
}

## ## PutObject permission from Target Bucket for Lambda
data "aws_iam_policy_document" "lambda_put_policy_doc" {
    statement {
      effect = "Allow"
      actions = [
        "s3:PutObject"
      ]
      resources = ["${aws_s3_bucket.target_bucket.arn}",
                  "${aws_s3_bucket.target_bucket.arn}/*"]
    }
}

## Policy for PutObject permission
resource "aws_iam_policy" "lambda_put_policy" {
    name_prefix = "lambda-put-"
    policy = data.aws_iam_policy_document.lambda_put_policy_doc.json

}

## Attachment for PutObject permission
resource "aws_iam_role_policy_attachment" "lambda_s3_put_attachment" {
    role = aws_iam_role.role_for_lambda.name
    policy_arn = resource.aws_iam_policy.lambda_put_policy.arn
}


## Assume Role for State Machine
data "aws_iam_policy_document" "assume_role_for_state_machine" {
    statement {
        effect = "Allow"
        
        principals {
          type = "Service"
          identifiers = ["states.amazonaws.com"]
        }

    actions = ["sts:AssumeRole"]
    }  
}

## Role for State Machine
resource "aws_iam_role" "role_for_state_machine" {
    name = "role_for_state_machine"
    assume_role_policy = data.aws_iam_policy_document.assume_role_for_state_machine.json
}

## Policy Document for State Machine to LambdaInvoke
data "aws_iam_policy_document" "state_machine_role_policy" {
  
  statement {
    effect = "Allow"

    actions = [
      "lambda:InvokeFunction"
    ]

    resources = ["${aws_lambda_function.lambda_func.arn}"]#["arn:aws:lambda:eu-west-2:750552037637:function:lambda_func"]
  }

}

## Policy for LambdaInvoke permission
resource "aws_iam_policy" "lambda_invoke_policy" {
    name_prefix = "lambda-invoke-"
    policy = data.aws_iam_policy_document.state_machine_role_policy.json

}

## Attachment for LambdaInvoke permission
resource "aws_iam_role_policy_attachment" "lambda_invoke_attachment" {
    role = aws_iam_role.role_for_state_machine.name
    policy_arn = resource.aws_iam_policy.lambda_invoke_policy.arn
}
