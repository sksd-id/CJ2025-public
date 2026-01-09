def main():
    questions = [
        {
            "question": "To begin with evaluating the incident, please provide the victim's OS + its version, and also the victim's computer name!",
            "format": "Windows 7 7.189.7sp1 WIN18910-18892"
        },
        {
            "question": "Where does this fake AV executable is being executed in the victim machine? Please provide the full path",
            "format": "D:\\where\\is\\it\\fake.exe"
        },
        {
            "question": "The malware seems to create a mutex in the victim's machine. What's the name of the Mutex? (Only provide the name without the path, case sensitive)",
            "format": "MutexName123"
        },
        {
            "question": "What's the main root directory that the malware seems to encrypt in the victim machine? Please provide the full path!",
            "format": "D:\\where\\is\\it"
        },
        {
            "question": "What's the original content of pw_manager.txt?",
            "format": "p4s5word123"
        }
    ]

    answers = [
        ["Windows 10 10.0.19041.1 DESKTOP-LCC9E2D","Windows 10 Version 19043 MP DESKTOP-LCC9E2D"],
        "C:\\Users\\USER\\Music\\Kaspersky.exe",
        "rnicrosoft",
        ["C:\\Users\\USER\\DokumenPenting","C:\\Users\\USER\\DokumenPenting\\"],
        "!h0peth3r34ren0m0r3ch34t!n94ft3rth15CTF"
    ]

    print("=" * 70)
    print("CASE 002: MALWARE ANALYSIS FORENSIC ON USER MACHINE --")
    print("=" * 70)
    print("\nPlease answer the following questions about the incident:\n")

    correct_answers = 0

    for index, q in enumerate(questions, start=1):
        print(f"\n{'=' * 70}")
        print(f"Question {index}/{len(questions)}:")
        print(f"{'=' * 70}")
        print(q["question"])
        print(f"\nFormat: {q['format']}")
        print("-" * 70)
        user_answer = input("Answer: ").strip()
        
        expected_answer = answers[index - 1]
        
        if index == 3:
            is_correct = user_answer == str(expected_answer)
        else:
            user_answer_lower = user_answer.lower()
            
            if isinstance(expected_answer, list):
                is_correct = any(user_answer_lower == str(ans).lower() for ans in expected_answer)
            else:
                is_correct = user_answer_lower == str(expected_answer).lower()
        
        if is_correct:
            correct_answers += 1
            print("Correct!")
        else:
            print("Incorrect!")
            return
    
    if correct_answers == len(questions):
        print("\n" + "=" * 70)
        print("INVESTIGATION COMPLETE!")
        print("=" * 70)
        print("\nGG!")
        print("\nFlag: CJ2025{th!s_is_the_beg1nnin9_0f_y0ur_4n4lysis_on_aPT_gr0up_a.k.a_as3ng_Persistent_Threat_anyway_the_malware_sucks_sorry}")
        print("\n" + "=" * 70)

if __name__ == "__main__":
    main()