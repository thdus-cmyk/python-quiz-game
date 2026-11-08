import random
from datetime import datetime

def play_quiz(game):
    """퀴즈 풀기 (랜덤 출제, 문제 수 선택, 힌트 및 점수 차감)"""
    if not game.quizzes:
        print("\n⚠️ 등록된 퀴즈가 없습니다. 퀴즈를 먼저 추가해주세요!")
        return
        
    total_available = len(game.quizzes)
    print(f"\n📝 퀴즈를 시작합니다! (등록된 총 문제 수: {total_available}개)")
    
    while True:
        cnt_str = input(f"풀고 싶은 문제 수를 입력하세요 (1 ~ {total_available}): ").strip()
        try:
            num_questions = int(cnt_str)
            if 1 <= num_questions <= total_available:
                break
            print(f"⚠️ 1에서 {total_available} 사이의 숫자를 입력하세요.")
        except ValueError:
            print("⚠️ 올바른 숫자를 입력하세요.")

    selected_quizzes = random.sample(game.quizzes, num_questions)
    correct_weighted_score = 0
    
    for idx, quiz in enumerate(selected_quizzes, 1):
        print("\n" + "-" * 40)
        print(f"[문제 {idx}/{num_questions}]")
        print(quiz.question)
        for i, choice in enumerate(quiz.choices, 1):
            print(f"{i}. {choice}")
            
        hint_used = False
        
        while True:
            ans_input = input("\n정답 번호 입력 (1~4) 또는 힌트 보기 ('h'): ").strip().lower()
            
            if ans_input == 'h':
                if not hint_used:
                    print(f"💡 [힌트]: {quiz.hint}")
                    hint_used = True
                else:
                    print("⚠️ 이미 이 문제에서 힌트를 사용하셨습니다!")
                continue
                
            if not ans_input:
                print("⚠️ 빈 입력입니다. 숫자를 입력하거나 'h'를 입력하세요.")
                continue
                
            try:
                ans = int(ans_input)
                if ans < 1 or ans > 4:
                    print("⚠️ 1~4 사이의 숫자를 입력하세요.")
                    continue
                break
            except ValueError:
                print("⚠️ 숫자 또는 'h'를 입력해주세요.")
                
        if quiz.check_answer(ans):
            print("✅ 정답입니다!")
            if hint_used:
                print("   (⚠️ 힌트를 사용하여 해당 문제는 0.5점 처리됩니다.)")
                correct_weighted_score += 0.5
            else:
                correct_weighted_score += 1.0
        else:
            print(f"❌ 틀렸습니다! 정답은 {quiz.answer}번입니다.")
            
    score = int((correct_weighted_score / num_questions) * 100)
    
    print("\n" + "=" * 40)
    print(f"🏆 결과: {num_questions}문제 중 맞춘 점수 환산 {score}점")
    print("=" * 40)
    
    if score > game.best_score:
        game.best_score = score
        print("🎉 새로운 최고 점수 달성!")

    now_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    history_record = {
        "date": now_time,
        "total": num_questions,
        "score": score
    }
    game.history.append(history_record)
    game.save_game_data()