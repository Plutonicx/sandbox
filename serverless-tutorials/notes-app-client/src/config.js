export default {
  MAX_ATTACHMENT_SIZE: 5000000,
    s3: {
      REGION: "ap-southeast-2",
      BUCKET: "stevan-notes-app-uploads"
    },
    apiGateway: {
      REGION: "ap-southeast-2",
      URL: "https://bv7phpku1d.execute-api.ap-southeast-2.amazonaws.com/prod"
    },
    cognito: {
      REGION: "ap-southeast-2",
      USER_POOL_ID: "ap-southeast-2_5Kqpo3M6L",
      APP_CLIENT_ID: "1i6dk642cts23k2vlaugti0vca",
      IDENTITY_POOL_ID: "ap-southeast-2:1e841aa1-cd43-4117-a41a-55ad66dedfb8"
    }
  };