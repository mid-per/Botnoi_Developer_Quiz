from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import (
    MessageEvent, TextMessage, TextSendMessage,
    ButtonsTemplate, TemplateSendMessage, PostbackAction,
    QuickReply, QuickReplyButton, CarouselTemplate, CarouselColumn
)

app = Flask(__name__)

# LINE Channel Access Token and Channel Secret
line_bot_api = LineBotApi('j8CgsyJm1019tc98Uj9DEbIxWK3JjvfKGxS8h4Qk826K9vWOb6fmZydEJzxCF3ZII/BY0Fb3El8Ls9uBIqGCtH08BziNQoKBNJK+KQfZ6/TKUT7u1SUcsNF/pomh//A4n51Z1IxZYH2l24MGyomuWwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a8dec9b9cff01e94ec1e3069477009fc')
#webhookapi with ngrok

# Root route for checking 
@app.route('/')
def index():
    return 'LINE Chatbot is running!'

# Webhook route
@app.route('/webhook', methods=['POST'])
def webhook():
    # Get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # Handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)

    return 'OK'

@handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    user_message = event.message.text

    if user_message == "text":
        # Reply with a text message
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="This is a text reply!")
        )

    elif user_message == "button":
        # Reply with a button template
        buttons_template = ButtonsTemplate(
            title="Button Template",
            text="Please select an option:",
            actions=[
                PostbackAction(label="Option 1", data="action=option1"),
                PostbackAction(label="Option 2", data="action=option2"),
            ]
        )
        template_message = TemplateSendMessage(
            alt_text="Buttons Template",
            template=buttons_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)

    elif user_message == "quickreply":
        # Reply with quick replies
        quick_reply_buttons = [
            QuickReplyButton(action=PostbackAction(label="Option 1", data="action=option1")),
            QuickReplyButton(action=PostbackAction(label="Option 2", data="action=option2")),
        ]
        quick_reply = QuickReply(items=quick_reply_buttons)
        text_message = TextSendMessage(text="Choose an option:", quick_reply=quick_reply)
        line_bot_api.reply_message(event.reply_token, text_message)

    elif user_message == "carousel":
        # Reply with a carousel template
        carousel_template = CarouselTemplate(
            columns=[
                CarouselColumn(
                    thumbnail_image_url="https://example.com/image1.jpg",
                    title="Carousel 1",
                    text="Description 1",
                    actions=[
                        PostbackAction(label="Button 1", data="action=carousel1_button1"),
                        PostbackAction(label="Button 2", data="action=carousel1_button2"),
                    ]
                ),
                CarouselColumn(
                    thumbnail_image_url="https://example.com/image2.jpg",
                    title="Carousel 2",
                    text="Description 2",
                    actions=[
                        PostbackAction(label="Button 1", data="action=carousel2_button1"),
                        PostbackAction(label="Button 2", data="action=carousel2_button2"),
                    ]
                ),
            ]
        )
        template_message = TemplateSendMessage(
            alt_text="Carousel Template",
            template=carousel_template
        )
        line_bot_api.reply_message(event.reply_token, template_message)

    else:
        # Default reply
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Please type 'text', 'button', 'quickreply', or 'carousel'.")
        )

if __name__ == '__main__':
    app.run(port=3000)
