## State Machine for Step Dunction for Lambda
resource "aws_sfn_state_machine" "sfn_state_machine" {
  name     = "state-machine-for-lambda"
  role_arn = aws_iam_role.iam_for_sfn.arn ## Work on this...

  definition = <<EOF
{
  "Comment": "A state machine to invoke the Lambda.",
  "StartAt": "Lambda Invoke",
  "States": {
    "Lambda Invoke": {
      "Type": "Task",
      "Resource": "${aws_lambda_function.lambda_func.arn}",
      "Output": "{% $states.result.Payload %}",
      "Arguments": {
        "FunctionName": "arn:aws:lambda:eu-west-2:750552037637:function:lambda_func:$LATEST",
        "Payload": "{% $states.input %}"
      },
      "Retry": [
        {
          "ErrorEquals": [
            "Lambda.ServiceException",
            "Lambda.AWSLambdaException",
            "Lambda.SdkClientException",
            "Lambda.TooManyRequestsException"
          ],
          "IntervalSeconds": 1,
          "MaxAttempts": 3,
          "BackoffRate": 2,
          "JitterStrategy": "FULL"
        }
      ],
      "End": true
    }
  },
  "QueryLanguage": "JSONata"
}
EOF
}