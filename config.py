# 竞赛项目配置规则
COMPETITION_RULES = {
    "编程挑战赛": {
        "无人机综合任务赛": {
            "allowed_levels": ["小学", "初中", "高中/职高（含中专）"],
            "participant_count": 1,
            "description": "适用学段：小学、中学"
        },
        "编程越障任务": {
            "allowed_levels": ["小学", "初中", "高中/职高（含中专）"],
            "participant_count": 1,
            "description": "适用学段：小学、初中、高中/职高"
        }
    },

    "第一视角飞行赛": {
        "多旋翼穿越任务": {
            "allowed_levels": ["小学", "初中", "高中/职高（含中专）"],
            "participant_count": 1,
            "description": "适用学段：小学、初中、高中/职高"
        },
        "无人机第一视角竞速（无刷组 A2）": {
            "allowed_levels": ["小学", "初中", "高中/职高（含中专）"],
            "participant_count": 1,
            "description": "适用学段：小学、初中、高中/职高"
        }
    },

    "飞行操控赛": {
        "个人越障任务": {
            "allowed_levels": ["小学", "初中", "高中/职高（含中专）"],
            "participant_count": 1,
            "description": "适用学段：小学、初中、高中/职高"
        },
        "无人机第三视角竞速": {
            "allowed_levels": ["小学", "初中", "高中/职高（含中专）"],
            "participant_count": 1,
            "description": "适用学段：小学、初中、高中/职高"
        },
        "超级进球手（200mm 空心杯）任务": {
            "allowed_levels": ["小学", "初中", "高中/职高（含中专）"],
            "participant_count": 1,
            "description": "适用学段：小学、中学"
        },
        "超级进球手（200mm 无刷）": {
            "allowed_levels": ["小学", "初中", "高中/职高（含中专）"],
            "participant_count": 1,
            "description": "适用学段：小学、中学"
        }
    },

    "空中对抗赛": {
        "无人机足球任务-3v3（200mm 空心杯）": {
            "allowed_levels": ["小学", "初中", "高中/职高（含中专）"],
            "participant_count": 3,
            "description": "适用学段：小学、中学"
        },
        "无人机足球任务-3v3（200mm 无刷）": {
            "allowed_levels": ["初中", "高中/职高（含中专）"],
            "participant_count": 3,
            "description": "适用学段：中学"
        },
        "无人机足球任务-5v5（400mm 无刷）": {
            "allowed_levels": ["初中", "高中/职高（含中专）"],
            "participant_count": 5,
            "description": "适用学段：中学"
        }
    },

    "应用场景飞行赛": {
        "装调运输任务": {
            "allowed_levels": ["小学", "初中", "高中/职高（含中专）"],
            "participant_count": 1,
            "description": "适用学段：小学、初中、高中/职高"
        },
        "空中狙击任务": {
            "allowed_levels": ["小学", "初中", "高中/职高（含中专）"],
            "participant_count": 1,
            "description": "适用学段：小学、初中、高中/职高"
        }
    }
}

# 学段选项
EDUCATION_LEVELS = ["小学", "初中", "高中/职高（含中专）"]

# 项目大类
CATEGORIES = list(COMPETITION_RULES.keys())

# 状态选项
APPLICATION_STATUS = ["pending", "approved", "rejected"]

# 获奖等级
AWARD_LEVELS = ["一等奖", "二等奖", "三等奖", "优秀奖"]
