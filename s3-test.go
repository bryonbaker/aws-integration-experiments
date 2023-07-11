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

	viper.SetConfigName("secrets")
	viper.SetConfigType("yaml")
	// Set the path to look for the config file
	viper.AddConfigPath(".")

	// Read the configuration file
	err := viper.ReadInConfig()
	if err != nil {
		panic(fmt.Errorf("failed to read configuration file: %s", err))
	}

	secretKey := viper.GetString("secretKey")
	accessKey := viper.GetString("accessKey")

	viper.SetConfigName("config")
	viper.SetConfigType("yaml")
	// Set the path to look for the config file
	viper.AddConfigPath(".")

	// Read the configuration file
	err = viper.ReadInConfig()
	if err != nil {
		panic(fmt.Errorf("failed to read configuration file: %s", err))
	}

	bucketName := viper.GetString("bucketName")

	// Read the file and extract the data
	fileName := "addresses2.txt"
	filePath := fileName
	data, err := os.Open(filePath)

	if err != nil {
		log.Fatal("Failed to read file:", err)
	}

	sess := CreateNewAWSSession(accessKey, secretKey)

	err = CreateBucket(sess, bucketName)
	if err != nil {
		log.Fatal("Failed to create bucket: ", err)
	}

	// Upload the data to S3 using AWS access keys
	uploadToS3(bucketName, fileName, data, sess)
}
