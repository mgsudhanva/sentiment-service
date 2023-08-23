FROM public.ecr.aws/lambda/python:3.11

COPY requirements.txt ./
RUN python3 -m pip install -r requirements.txt --target ${LAMBDA_TASK_ROOT}

COPY ./ ${LAMBDA_TASK_ROOT}/

CMD [ "handler.handler" ]