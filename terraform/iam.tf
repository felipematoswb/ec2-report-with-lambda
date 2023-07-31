resource "aws_iam_role" "lambda-role-for-access-ec2-and-cloudwatch" {
	name = "lambda-role-for-access-ec2-and-cloudwatch"
	assume_role_policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = "sts:AssumeRole"
            Effect = "Allow"
            Sid    = ""
            Principal = {
                Service = "lambda.amazonaws.com"
            }
        },
        ]
    })
    tags = {
        terraform = "true"
    }
}

resource "aws_iam_policy" "lambda-policy-for-access-ec2-and-cloudwatch" {
	name        = "lambda-policy-for-access-ec2-and-cloudwatch"
	path        = "/"
	description = "IAM policy for logging from a lambda"
    policy = jsonencode({
        Version = "2012-10-17"
        Statement = [
        {
            Action = [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents",
            ]
            Effect   = "Allow"
            Resource = [
                "arn:aws:logs:*:*:*",
            ]
        },
        {
            Effect = "Allow",
            Action = [
                "xray:PutTraceSegments",
                "xray:PutTelemetryRecords",
                "xray:GetSamplingRules",
                "xray:GetSamplingTargets",
                "xray:GetSamplingStatisticSummaries"
            ],
            Resource = [
                "*"
            ]
        },
        {
            Action = [
                "ec2:*",
            ]
            Effect   = "Allow"
            Resource = [
                "*"
            ]
        }
        ]
    })
    tags = {
        terraform = "true"
    }
}

resource "aws_iam_role_policy_attachment" "lambda-attach-for-access-ec2-and-cloudwatch" {
	role       = aws_iam_role.lambda-role-for-access-ec2-and-cloudwatch.name
	policy_arn = aws_iam_policy.lambda-policy-for-access-ec2-and-cloudwatch.arn
}