import json

mbti_db = {
    "ISTJ": {"name": "청렴결백한 논리주의자 (잇티제)", "desc": "매사에 철저하고 계획적이며 현실적인 성격입니다."},
    "ISFJ": {"name": "용감한 수호자 (잇프제)", "desc": "따뜻하고 헌신적이며 타인을 잘 배려하는 성격입니다."},
    "INFJ": {"name": "선의의 옹호자 (인프제)", "desc": "통찰력이 높고 조용하며 자신의 신념이 뚜렷합니다."},
    "INTJ": {"name": "용의주도한 전략가 (인티제)", "desc": "분석적이고 효율을 중요시하는 아이디어 뱅크입니다."},
    "ISTP": {"name": "만능 재주꾼 (잇팁)", "desc": "도구 사용에 능하고 관찰력이 뛰어난 실용적인 성격입니다."},
    "ISFP": {"name": "호기심 많은 예술가 (잇프피)", "desc": "온화하고 친절하며 미적 감각이 뛰어납니다."},
    "INFP": {"name": "열정적인 중재자 (인프피)", "desc": "감수성이 풍부하고 혼자만의 시간을 소중히 여기는 내면의 평화주의자입니다."},
    "INTP": {"name": "논리적인 사색가 (인팁)", "desc": "지적 호기심이 많고 분석적인 사고를 즐깁니다."},
    "ESTP": {"name": "모험을 즐기는 사업가 (엣팁)", "desc": "활동적이고 사교적이며 위기 대처 능력이 뛰어납니다."},
    "ESFP": {"name": "자유로운 영혼의 연예인 (엣프피)", "desc": "에너지가 넘치고 사람들과 어울리는 것을 좋아하는 분위기 메이커입니다."},
    "ENFP": {"name": "재기발랄한 활동가 (엔프피)", "desc": "창의적이고 열정적이며 사람들에게 긍정적인 에너지를 줍니다."},
    "ENTP": {"name": "뜨거운 논쟁을 즐기는 변론가 (엔팁)", "desc": "도전을 좋아하고 창의적인 아이디어가 넘치는 토론가입니다."},
    "ESTJ": {"name": "엄격한 관리자 (엣티제)", "desc": "리더십이 강하고 질서 정연하며 책임감이 투철합니다."},
    "ESFJ": {"name": "사교적인 외교관 (엣프제)", "desc": "친절하고 사교적이며 사람들과의 관계를 중시합니다."},
    "ENFJ": {"name": "정의로운 사회운동가 (엔프제)", "desc": "카리스마가 있고 사람들을 이끄는 리더십이 강합니다."},
    "ENTJ": {"name": "대담한 통솔자 (엔티제)", "desc": "의지가 강하고 효율을 중시하며 목표 지향적입니다."}
}

blood_db = {
    "A형": {
        "title": "신중하고 배려심 깊은 평화주의자",
        "desc": "꼼꼼하고 배려심이 뛰어난 성격입니다. 규칙과 질서를 잘 지키며 타인의 감정을 헤아리는 데 탁월합니다. 다만, 자신의 마음을 드러내는 것을 조심스러워하며 내적으로 걱정이 많을 수 있습니다.",
        "traits": ["배려심 깊음", "신중함", "성실함", "완벽주의"],
        "compatibility": {
            "best": ["O형", "A형"],
            "good": ["AB형"],
            "bad": ["B형"]
        }
    },
    "B형": {
        "title": "자유분방하고 창의적인 개성파",
        "desc": "주관이 뚜렷하고 아이디어가 풍부한 자유로운 영혼입니다. 흥미를 느끼는 분야에 엄청난 집중력을 발휘하며, 솔직하고 털털한 소통 방식을 지녔습니다. 간섭이나 구속받는 것을 싫어합니다.",
        "traits": ["자유분방", "창의적", "솔직함", "주관 뚜렷"],
        "compatibility": {
            "best": ["O형", "AB형"],
            "good": ["B형"],
            "bad": ["A형"]
        }
    },
    "O형": {
        "title": "활발하고 사교적인 리더형",
        "desc": "친화력이 뛰어나고 성격이 낙천적이며 대범합니다. 리더십이 강해 모임을 주도하거나 타인을 돕는 것을 좋아합니다. 솔직하고 뒤끝이 없는 편이지만, 의외로 쓸쓸함을 잘 탈 때도 있습니다.",
        "traits": ["사교성", "리더십", "낙천적", "솔직담백"],
        "compatibility": {
            "best": ["A형", "B형", "O형"],
            "good": ["AB형"],
            "bad": []
        }
    },
    "AB형": {
        "title": "합리적이고 분석적인 평화주의자",
        "desc": "지적이고 냉철하며 공사의 구분이 뚜렷한 성격입니다. 분석적이고 합리적인 선택을 선호하며, 갈등을 싫어하는 평화주의자입니다. 사생활을 매우 중요시하며 감정 변화를 잘 드러내지 않습니다.",
        "traits": ["합리적", "분석적", "개인주의", "감정 조절"],
        "compatibility": {
            "best": ["AB형"],
            "good": ["A형", "B형", "O형"],
            "bad": []
        }
    }
}

mbti_compatibility_db = {
    "ISTJ": {
        "best": ["ESFP", "ESTP"],
        "good": ["ISFJ", "ESTJ", "INTJ", "ISTP"],
        "bad": ["ENFP", "ENTP", "INFP"]
    },
    "ISFJ": {
        "best": ["ESFP", "ESTP"],
        "good": ["ISTJ", "ESFJ", "ISFP"],
        "bad": ["ENTP", "ENFP", "INTP"]
    },
    "INFJ": {
        "best": ["ENFP", "ENTP"],
        "good": ["INFP", "INTJ", "ENFJ"],
        "bad": ["ESTP", "ESFP", "ISTP"]
    },
    "INTJ": {
        "best": ["ENFP", "ENTP"],
        "good": ["INFJ", "ENTJ", "ISTJ", "INTP"],
        "bad": ["ESFP", "ESTP", "ISFP"]
    },
    "ISTP": {
        "best": ["ESFJ", "ESTJ"],
        "good": ["ISTJ", "ESTP", "INTP"],
        "bad": ["ENFJ", "INFJ", "ENFP"]
    },
    "ISFP": {
        "best": ["ENFJ", "ESFJ", "ESTJ"],
        "good": ["ISFJ", "INFP", "ESFP"],
        "bad": ["INTJ", "ENTJ", "ENTP"]
    },
    "INFP": {
        "best": ["ENFJ", "ENTJ"],
        "good": ["INFJ", "ISFP", "INTP"],
        "bad": ["ISTJ", "ESTJ", "ESTP"]
    },
    "INTP": {
        "best": ["ENTJ", "ESTJ"],
        "good": ["INTJ", "ENTP", "INFP", "ISTP"],
        "bad": ["ESFJ", "ISFJ", "ESFP"]
    },
    "ESTP": {
        "best": ["ISFJ", "ISTJ"],
        "good": ["ESFP", "ISTP", "ESTJ"],
        "bad": ["INFJ", "INFP", "ENFJ"]
    },
    "ESFP": {
        "best": ["ISFJ", "ISTJ"],
        "good": ["ESTP", "ESFJ", "ISFP"],
        "bad": ["INTJ", "INTP", "INFJ"]
    },
    "ENFP": {
        "best": ["INFJ", "INTJ"],
        "good": ["ENFJ", "ENTP", "INFP"],
        "bad": ["ISTJ", "ISTP", "ESTJ"]
    },
    "ENTP": {
        "best": ["INFJ", "INTJ"],
        "good": ["ENFP", "INTP", "ENTJ"],
        "bad": ["ISFJ", "ISFP", "ESFJ"]
    },
    "ESTJ": {
        "best": ["ISTP", "ISFP", "INTP"],
        "good": ["ISTJ", "ESTP", "ENTJ"],
        "bad": ["INFP", "ENFP", "INFJ"]
    },
    "ESFJ": {
        "best": ["ISTP", "ISFP"],
        "good": ["ISFJ", "ESFP", "ENFJ"],
        "bad": ["INTP", "ENTP", "INTJ"]
    },
    "ENFJ": {
        "best": ["INFP", "ISFP"],
        "good": ["INFJ", "ENFP", "ESFJ"],
        "bad": ["ISTP", "ESTP", "INTP"]
    },
    "ENTJ": {
        "best": ["INFP", "INTP"],
        "good": ["INTJ", "ENTP", "ESTJ"],
        "bad": ["ISFP", "ESFP", "ISFJ"]
    }
}

data = {
    "mbti_db": mbti_db,
    "blood_db": blood_db,
    "mbti_compatibility_db": mbti_compatibility_db
}

with open("mbti_data.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=4)
