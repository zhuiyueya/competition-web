import os

def _seed_default_templates():
    from models import CertificateTemplate

    existing_count = CertificateTemplate.query.count()
    if existing_count and existing_count > 0:
        return

    player = CertificateTemplate(
        name='选手版-一等奖(默认)',
        category='通用',
        award_level='一等奖'
    )
    player.set_config({
        'background_image': 'assets/cert/player.png',
        'debug_points': False,
        'texts': []
    })

    coach = CertificateTemplate(
        name='辅导员版-一等奖(默认)',
        category='通用',
        award_level='一等奖-辅导员'
    )
    coach.set_config({
        'background_image': 'assets/cert/player.png',
        'debug_points': False,
        'texts': []
    })

    from app import db
    db.session.add(player)
    db.session.add(coach)
    db.session.commit()


def main():
    from app import app, db
    import models  # noqa: F401

    with app.app_context():
        db.create_all()
        try:
            _seed_default_templates()
        except Exception:
            db.session.rollback()
            raise


if __name__ == '__main__':
    main()
