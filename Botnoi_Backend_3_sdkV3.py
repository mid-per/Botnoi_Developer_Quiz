import os
from flask import Flask, request, abort
from linebot.v3 import WebhookHandler
from linebot.v3.exceptions import InvalidSignatureError
from linebot.v3.messaging import (
    Configuration,
    ApiClient,
    MessagingApi,
    ReplyMessageRequest,
    TextMessage,
    TemplateMessage,
    ButtonsTemplate,
    PostbackAction,
    QuickReply,
    QuickReplyItem,
    CarouselTemplate,
    CarouselColumn
)
from linebot.v3.webhooks import MessageEvent, TextMessageContent

app = Flask(__name__)

configuration = Configuration(access_token='j8CgsyJm1019tc98Uj9DEbIxWK3JjvfKGxS8h4Qk826K9vWOb6fmZydEJzxCF3ZII/BY0Fb3El8Ls9uBIqGCtH08BziNQoKBNJK+KQfZ6/TKUT7u1SUcsNF/pomh//A4n51Z1IxZYH2l24MGyomuWwdB04t89/1O/w1cDnyilFU=')
handler = WebhookHandler('a8dec9b9cff01e94ec1e3069477009fc')

IMAGE_PATHS = {
    'image1': 'assets/image1.jpg',  
    'image2': 'assets/image2.jpg'   
}

def upload_image_to_line(image_path):
    """Upload image to LINE's temporary storage and return URL"""
    if not os.path.exists(image_path):
        raise FileNotFoundError(f"Image file not found: {image_path}")
    
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        with open(image_path, 'rb') as f:
            # Note: We're using rich menu endpoint as it's the only upload endpoint available
            response = line_bot_api.upload_rich_menu_image(
                rich_menu_id='dummy',  # Not actually used for our purpose
                body=f
            )
            return response.content_url

@app.route("/callback", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    user_message = event.message.text

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)

        if user_message == "text":
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="This is a text reply!")]
                )
            )

        elif user_message == "button":
            message = TemplateMessage(
                alt_text="Buttons Template",
                template=ButtonsTemplate(
                    title="Button Template",
                    text="Please select an option:",
                    actions=[
                        PostbackAction(label="Option 1", data="action=option1"),
                        PostbackAction(label="Option 2", data="action=option2"),
                    ]
                )
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[message]
                )
            )

        elif user_message == "quickreply":
            message = TextMessage(
                text="Choose an option:",
                quick_reply=QuickReply(
                    items=[
                        QuickReplyItem(action=PostbackAction(label="Option 1", data="action=option1")),
                        QuickReplyItem(action=PostbackAction(label="Option 2", data="action=option2")),
                    ]
                )
            )
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[message]
                )
            )

        elif user_message == "carousel":
            try:
                # Upload images to LINE's server
                image1_url = upload_image_to_line(IMAGE_PATHS['image1'])
                image2_url = upload_image_to_line(IMAGE_PATHS['image2'])
                
                message = TemplateMessage(
                    alt_text="Carousel Template",
                    template=CarouselTemplate(
                        columns=[
                            CarouselColumn(
                                thumbnail_image_url=image1_url,
                                title="Carousel 1",
                                text="Description 1",
                                actions=[
                                    PostbackAction(label="Button 1", data="action=carousel1_button1"),
                                    PostbackAction(label="Button 2", data="action=carousel1_button2"),
                                ]
                            ),
                            CarouselColumn(
                                thumbnail_image_url=image2_url,
                                title="Carousel 2",
                                text="Description 2",
                                actions=[
                                    PostbackAction(label="Button 1", data="action=carousel2_button1"),
                                    PostbackAction(label="Button 2", data="action=carousel2_button2"),
                                ]
                            ),
                        ]
                    )
                )
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[message]
                    )
                )
            except Exception as e:
                app.logger.error(f"Failed to create carousel: {str(e)}")
                line_bot_api.reply_message(
                    ReplyMessageRequest(
                        reply_token=event.reply_token,
                        messages=[TextMessage(text="Failed to load carousel. Please try again.")]
                    )
                )

        else:
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    reply_token=event.reply_token,
                    messages=[TextMessage(text="Please type 'text', 'button', 'quickreply', or 'carousel'.")]
                )
            )

if __name__ == "__main__":
    # Create assets directory if it doesn't exist
    if not os.path.exists('assets'):
        os.makedirs('assets')
    app.run(port=3000)