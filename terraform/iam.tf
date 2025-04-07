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