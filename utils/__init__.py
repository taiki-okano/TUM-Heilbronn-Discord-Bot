from course_specification_template import COURSE_SPECIFICATION_TEMPLATE
from registration_mail_template import REGISTRATION_MAIL_TEMPLATE
from welcome_msg_template import WELCOME_MSG_TEMPLATE
from email_sender import send_email
from secrets import DISCORD_TOKEN, SMTP_EMAIL, SMTP_HOSTNAME, SMTP_USER, SMTP_PASSWORD, GUILD_ID
from constants import COURSE_CODE_TO_ROLENAME, TUM_STUDENT_ROLE_NAME, GUEST_ROLE_NAME, COURSE_ROLE_IDS