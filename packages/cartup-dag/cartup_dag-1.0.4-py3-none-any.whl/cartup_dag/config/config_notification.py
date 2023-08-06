notifications = {
    "email": {"smtp_server": "smtp.office365.com",
              "port": 587,
              "sender_email": "ops@cartup.ai",
              "password": "CartUp@123$",
              "email_list": ["shyam@cartup.ai", "preethi@cartup.ai", "arvind@cartup.ai"],
              "udf": "notifications.udf_notifications.UDF_Notification.send_message_to_Email_teams"
              },
    "ms_teams": {
        "webhook": "https://cartup941.webhook.office.com/webhookb2/d4281ef6-3ea5-470d-86d6-7d8b0d7cd747@a120f05c-ec16-43a4-96f9-823ace590f3e/IncomingWebhook/9b2bc7e39ef749218c1a802af381118e/63137dc6-9b59-4725-9522-daa40324ddd1",
        "udf": "notifications.udf_notifications.UDF_Notification.send_message_to_MS_teams"

    },
    "send_grid": {

    },
    "sms": {
        "account_sid": "AC1fb6307a9398805041de9bc3309f3c32",
        "auth_token": "724f2741d86acf1883d638684ad10f47",
        "from_number": "+1 7152652405 ",
        "receiver_list": ["+1 4088213257"],
        "udf": "notifications.udf_notifications.UDF_Notification.send_message_to_SMS_teams"
    }
}

s3_config = {
    "region": "us-east-1",
    "endpoint_url": "https://nyc3.digitaloceanspaces.com",
    "ACCESS_ID": 'DO00XZYD4G3D28JVRPCQ',
    "SECRET_KEY": 'dHP65XVtDpR0nY2WDGJDxJ5Gtsc2TA/NxqJsP8xm+tc'
}
