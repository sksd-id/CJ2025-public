def main():
    questions = [
        {
            "question": "From where did the attacker first obtain sensitive info from the public site?",
            "format": "Admin.sql"
        },
        {
            "question": "When was the sensitive file first accessed? (Format: YYYY-MM-DD HH:MM:SS UTC)",
            "format": "2025-01-01 00:00:00 UTC"
        },
        {
            "question": "What is the CloudFront request ID for the sensitive file access?",
            "format": "1A2B3C4D5E6F7"
        },
        {
            "question": "Which IAM user does the leaked access key belong to?",
            "format": "Example-User"
        },
        {
            "question": "What is the access key ID of the compromised IAM user?",
            "format": "AKIA1A2B3C4D5E6F7G8H"
        },
        {
            "question": "What AWS region was used for the attack?",
            "format": "us-east-1"
        },
        {
            "question": "What was the first API call made using the stolen key?",
            "format": "aws:ExampleCall"
        },
        {
            "question": "When did the attacker first use the stolen credentials? (Format: YYYY-MM-DD HH:MM:SS UTC)",
            "format": "2025-01-01 00:00:00 UTC"
        },
        {
            "question": "Which tool was used for AWS reconnaissance?",
            "format": "example-tool"
        },
        {
            "question": "What is the weak IAM policy statement?",
            "format": "IAMPolicyStatement"
        },
        {
            "question": "Which IAM user was created for privilege escalation?",
            "format": "Example-User"
        },
        {
            "question": "When did the attacker first access the created backdoor user? (Format: YYYY-MM-DD HH:MM:SS UTC)",
            "format": "2025-01-01 00:00:00 UTC"
        },
        {
            "question": "What is the access key ID of the backdoor user?",
            "format": "AKIA1A2B3C4D5E6F7G8H"
        },
        {
            "question": "What is the source IP address when the backdoor user first accessed AWS?",
            "format": "123.123.123.123"
        },
        {
            "question": "Which country is the attacker located in?",
            "format": "CountryName"
        }
    ]

    answers = [
        ".env",
        "2025-12-07 05:22:12 UTC",
        "46JVQE57VA61FVNS",
        "cloudserve",
        "AKIA453N4QOMPG2YR45P",
        "ap-southeast-1",
        ["sts:GetCallerIdentity", "GetCallerIdentity"],
        "2025-12-07 05:27:08 UTC",
        ["aws-enumerator", "aws_enumerator"],
        "ManageCloudServeUsers",
        "cloudserve-bot",
        "2025-12-07 05:45:54 UTC",
        "AKIA453N4QOMJWZXIPOB",
        "185.184.192.247",
        "Netherlands"
    ]

    print("Please answer the following investigation questions:")

    correct_answers = 0

    for index, q in enumerate(questions, start=1):
        print(f"\nQuestion {index}:")
        print(q["question"])
        print("Format: " + q["format"])
        user_answer = input("Answer: ").strip()
        
        expected_answer = answers[index - 1]
        user_answer_lower = user_answer.lower()
        
        # Check if answer is a list (array of acceptable answers)
        if isinstance(expected_answer, list):
            is_correct = any(user_answer_lower == str(ans).lower() for ans in expected_answer)
        else:
            is_correct = user_answer_lower == str(expected_answer).lower()
        
        if is_correct:
            correct_answers += 1
            print("Correct")
        else:
            print("Incorrect")
            return
    
    if correct_answers == len(questions):
        print("\nCongrats! Flag: CJ2025{yeah_never_push_your_env_files_to_prod}")

if __name__ == "__main__":
    main()