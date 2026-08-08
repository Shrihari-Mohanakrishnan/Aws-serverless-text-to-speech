# AWS Serverless Text-to-Speech Converter

## Executive Summary

This project implements an event-driven, serverless text-to-speech pipeline using Amazon S3, AWS Lambda, and Amazon Polly.

A text file uploaded to an Amazon S3 input bucket automatically triggers an AWS Lambda function. The function retrieves the uploaded text, submits it to Amazon Polly for speech synthesis, and stores the resulting MP3 audio in a dedicated S3 output bucket.

The implementation demonstrates how managed AWS services can be integrated to build an automated processing workflow without provisioning or managing application servers.

## Objectives

The project was designed with the following objectives:

- Automate the conversion of text files into speech without manual processing.
- Implement an event-driven workflow using Amazon S3 and AWS Lambda.
- Integrate Amazon Polly into a serverless application for speech synthesis.
- Separate input and generated output using dedicated S3 buckets.
- Apply IAM-based access control between the AWS services involved.
- Validate the complete workflow from file upload to playable MP3 output.

## Technology Stack

| Technology | Role |
|---|---|
| **Amazon S3** | Input and output object storage |
| **AWS Lambda** | Serverless application logic |
| **Amazon Polly** | Text-to-speech synthesis |
| **AWS IAM** | Service permissions and access control |
| **Python** | Lambda implementation language |
| **Boto3** | AWS SDK used by the Lambda function |

## Implementation Steps

1. **Created the S3 input bucket**
   - Created `cloud-user-upload-bucket`.
   - This bucket is used to receive `.txt` files for processing.

2. **Created the S3 output bucket**
   - Created `cloud-user-result-bucket`.
   - This bucket is used to store the generated MP3 files.

3. **Created the IAM permissions**
   - Configured the Lambda execution role with permissions required to interact with S3 and Amazon Polly.
   - Enabled Lambda to read input files, generate speech using Polly, write output files.

4. **Created the AWS Lambda function**
   - Created the Lambda function using Python.
   - The function acts as the processing layer between S3 and Amazon Polly.
   - Configured the function to use the required IAM execution role.

5. **Configured the S3 event notification**
   - Configured the input S3 bucket to send an event when a new object is created.
   - Added `.txt` as the suffix filter.
   - Connected the event notification to the Lambda function.
   - This allows the conversion process to start automatically when a text file is uploaded.

6. **Implemented the S3 file retrieval logic**
   - Used `boto3` to retrieve the uploaded text file from the input bucket.
   - Extracted the object key from the S3 event.
   - Read the file contents as UTF-8 text.

7. **Integrated Amazon Polly**
   - Configured the Lambda function to send the extracted text to Amazon Polly.
   - Used the `SynthesizeSpeech` API.
     
8. **Implemented MP3 output generation**
   - Derived the output filename from the original `.txt` filename.
   - For example:
     - `Uploadthis.txt` → `Uploadthisss.mp3`
   - Received the generated audio as a stream from Amazon Polly.

9. **Stored the generated audio**
   - Uploaded the Polly audio stream to `cloud-user-result-bucket`.
   - Set the object content type to `audio/mpeg`.

10. **Tested the complete workflow**
    - Created a sample `.txt` file.
    - Uploaded the file to `cloud-user-upload-bucket`.
    - Verified that the S3 event triggered the Lambda function.
    - Verified that Lambda successfully called Amazon Polly.
    - Checked the output bucket for the generated `.mp3` file.
    - Downloaded the MP3 file and verified that it could be played successfully.

11. **Troubleshot and resolved implementation issues**
    - Investigated an initially downloaded S3 object that was identified as JSON rather than audio.
    - Determined that the object was related to the Lambda asynchronous invocation result rather than the Polly-generated MP3.
    - Also resolved an S3 event notification conflict caused by an existing `.txt` object-created rule.
    - Re-tested the workflow after the corrections and confirmed successful MP3 generation.

## Architecture & System Design

The application follows an event-driven serverless architecture. Amazon S3 acts as the entry point for the workflow, while AWS Lambda performs the processing and Amazon Polly provides the speech synthesis capability.

The system uses two separate S3 buckets:

- **Input bucket:** `cloud-user-upload-bucket`
- **Output bucket:** `cloud-user-result-bucket`

This separation keeps the original text input independent from the generated audio output.


```text
┌──────────────────────┐
│        User          │
│                      │
│ Uploads .txt file    │
└──────────┬───────────┘
           │
           │ Object upload
           ▼
┌──────────────────────┐
│      Amazon S3        │
│   Input Bucket       │
│                      │
│ cloud-user-upload-   │
│ bucket               │
└──────────┬───────────┘
           │
           │ Object Created Event
           ▼
┌──────────────────────┐
│      AWS Lambda      │
│                      │
│ Python + Boto3       │
└──────────┬───────────┘
           │
           │ Text
           ▼
┌──────────────────────┐
│     Amazon Polly     │
│                      │
│   Text → Speech      │
└──────────┬───────────┘
           │
           │ MP3 Audio Stream
           ▼
┌──────────────────────┐
│      Amazon S3       │
│    Output Bucket     │
│                      │
│ cloud-user-result-   │
│ bucket               │
└──────────────────────┘


