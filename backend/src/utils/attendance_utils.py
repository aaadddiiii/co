from datetime import datetime
from src.db.model import Schedule
from src.core.logger import logger



def is_valid_teaching_time(teacher_id, class_id, period):
    from datetime import datetime

    now = datetime.now()
    current_day = now.strftime("%A")
    current_time = now.time()

    sched = Schedule.query.filter_by(
        teacher_id=teacher_id,
        class_id=class_id,
        period=period,
        day=current_day
    ).first()

    logger.info(f"{teacher_id} {class_id} {period} {current_day}")

    if not sched:
        return False

    return sched.start_time <= current_time <= sched.end_time