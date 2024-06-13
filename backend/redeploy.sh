#!/bin/bash

# Enable echoing of commands
# set -x

#to avoid nano or other pagers
export PAGER=cat

# Variables
AWS_REGION=us-west-2
ECR_REPOSITORY=775645845343.dkr.ecr.$AWS_REGION.amazonaws.com/search-app
ECS_CLUSTER_NAME=search-api-cluster
ECS_SERVICE_NAME=search-api-arm-service-elb
ECS_TASK_DEFINITION_NAME=search-api-arm-task

# Build, Tag and push the updated Docker image
aws ecr get-login-password --region us-west-2 | docker login --username AWS --password-stdin 775645845343.dkr.ecr.us-west-2.amazonaws.com
docker build -t search-app .  
docker tag search-app:latest $ECR_REPOSITORY:latest
docker push $ECR_REPOSITORY:latest

# Create a new task definition revision
TASK_DEFINITION_JSON=$(aws ecs describe-task-definition --task-definition $ECS_TASK_DEFINITION_NAME)
#echo $TASK_DEFINITION_JSON
NEW_TASK_DEFINITION_JSON=$(echo $TASK_DEFINITION_JSON | jq --arg IMAGE "$ECR_REPOSITORY:latest" --arg OPENAI_API_KEY "$OPENAI_API_KEY" '
.taskDefinition |
.containerDefinitions[0].image = $IMAGE |
.containerDefinitions[0].environment += [{"name": "OPENAI_API_KEY", "value": $OPENAI_API_KEY}] |
{
  family: .family,
  containerDefinitions: .containerDefinitions,
  executionRoleArn: .executionRoleArn,
  networkMode: .networkMode,
  requiresCompatibilities: .requiresCompatibilities,
  cpu: .cpu,
  memory: .memory,
  runtimePlatform: .runtimePlatform
}')
#echo $NEW_TASK_DEFINITION_JSON
# Register the new task definition revision
NEW_TASK_DEFINITION=$(aws ecs register-task-definition --cli-input-json "$NEW_TASK_DEFINITION_JSON")
#echo $NEW_TASK_DEFINITION
# Update the ECS service to use the new task definition revision
NEW_TASK_DEFINITION_REVISION=$(echo $NEW_TASK_DEFINITION | jq -r '.taskDefinition.taskDefinitionArn')
#echo $NEW_TASK_DEFINITION_REVISION
aws ecs update-service --cluster $ECS_CLUSTER_NAME --service $ECS_SERVICE_NAME --task-definition $NEW_TASK_DEFINITION_REVISION
