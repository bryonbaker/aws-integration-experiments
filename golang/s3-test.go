package main

import (
	"fmt"
	"log"
	"os"

	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/credentials"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"github.com/spf13/viper"
)

func CreateNewAWSSession(accessKey string, secretKey string) *session.Session {
	// Create a new AWS session with the provided access keys
	sess, err := session.NewSession(&aws.Config{
		Region:      aws.String("us-east-1"), // Replace with your desired AWS region
		Credentials: credentials.NewStaticCredentials(accessKey, secretKey, ""),
	})

	if err != nil {
		log.Fatal("Failed to create AWS session:", err)
	}

	return sess
}

func CreateBucket(sess *session.Session, bucketName string) error {
	svc := s3.New(sess)

	_, err := svc.CreateBucket(&s3.CreateBucketInput{
		Bucket: aws.String(bucketName),
	})

	return err
}

func uploadToS3(bucketName, fileName string, data *os.File, sess *session.Session) {
	svc := s3.New(sess)

	// Upload data to S3
	_, err := svc.PutObject(&s3.PutObjectInput{
		Body:   aws.ReadSeekCloser(data),
		Bucket: aws.String(bucketName),
		Key:    aws.String(fileName),
	})

	if err != nil {
		log.Fatal("Failed to upload data to S3:", err)
	}

	fmt.Printf("Data uploaded successfully to s3://%s/%s\n", bucketName, fileName)
}

func main() {
	// Get the secret from somewhere out of version control
	home := os.Getenv("HOME")
	if home == "" {
		fmt.Println("$HOME is not set.")
	} else {
		fmt.Printf("The value of $HOME is: %s\n", home)
	}

	// Read the Secrets file
	viper.SetConfigName("secrets")
	viper.SetConfigType("yaml")
	// Set the path to look for the config file
	viper.AddConfigPath(home)

	err := viper.ReadInConfig()
	if err != nil {
		panic(fmt.Errorf("failed to read configuration file: %s", err))
	}

	secretAccessKey := viper.GetString("secretAccessKey")
	accessKey := viper.GetString("accessKey")

	// Read the configuration file from the current directory
	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	// Set the path to look for the config file
	viper.AddConfigPath(".")

	err = viper.ReadInConfig()
	if err != nil {
		panic(fmt.Errorf("failed to read configuration file: %s", err))
	}

	fmt.Printf("AWS access key: %s\nAWS Secret Access Key: %s\n", accessKey, secretAccessKey)

	bucketName := viper.GetString("bucketName")
	fileName := viper.GetString("fileName")

	// Read the file and extract the data
	filePath := fileName
	data, err := os.Open(filePath)

	if err != nil {
		log.Fatal("Failed to read file:", err)
	}
	fmt.Printf("Bucket name: %s\nFilename: %s\n", bucketName, fileName)

	sess := CreateNewAWSSession(accessKey, secretAccessKey)

	fmt.Printf("Creating bucket: %s\n", bucketName)
	err = CreateBucket(sess, bucketName)
	if err != nil {
		log.Fatal("Failed to create bucket: ", err)
	}

	// Upload the data to S3 using AWS access keys
	fmt.Printf("Uploading %s\n", fileName)
	uploadToS3(bucketName, fileName, data, sess)
}
