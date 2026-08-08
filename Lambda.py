import boto3
import json
import logging
from urllib.parse import unquote_plus

logger = logging.getLogger()
logger.setLevel(logging.INFO)

s3 = boto3.client('s3')
polly = boto3.client('polly')


def lambda_handler(event, context):

    
    source_bucket = 'cloud-user-upload-bucket'
    destination_bucket = 'cloud-user-result-bucket'

   
    text_file_key = unquote_plus(
        event['Records'][0]['s3']['object']['key']
    )

    
    audio_key = text_file_key.rsplit('.', 1)[0] + '.mp3'

    try:
        
        logger.info(
            f"Reading file: s3://{source_bucket}/{text_file_key}"
        )

        response = s3.get_object(
            Bucket=source_bucket,
            Key=text_file_key
        )

        text = response['Body'].read().decode('utf-8')

        
        logger.info("Sending text to Amazon Polly")

        polly_response = polly.synthesize_speech(
            Text=text,
            OutputFormat='mp3',
            VoiceId='Joanna'
        )

        
        if 'AudioStream' in polly_response:

            logger.info(
                f"Uploading audio to: "
                f"s3://{destination_bucket}/{audio_key}"
            )

            s3.upload_fileobj(
                polly_response['AudioStream'],
                destination_bucket,
                audio_key,
                ExtraArgs={
                    'ContentType': 'audio/mpeg'
                }
            )

        logger.info(
            f"Text-to-Speech conversion completed successfully: "
            f"{audio_key}"
        )

        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Text-to-Speech conversion completed successfully',
                'audio_file': f's3://{destination_bucket}/{audio_key}'
            })
        }

    except Exception as e:

        logger.error(
            f"Error processing {text_file_key}: {str(e)}",
            exc_info=True
        )

        raise