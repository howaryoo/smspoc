FROM rabbitmq:3.7.4-management

RUN apt-get update && \
    apt-get install -y \
        curl \
        vim \
        netcat \
        unzip

RUN curl https://dl.bintray.com/rabbitmq/community-plugins/3.7.x/rabbitmq_delayed_message_exchange/rabbitmq_delayed_message_exchange-20171201-3.7.x.zip > /tmp/dmx3.7.zip && \
    unzip -d $RABBITMQ_HOME/plugins/ /tmp/dmx3.7.zip && \
    rabbitmq-plugins enable --offline rabbitmq_delayed_message_exchange && \
    rabbitmq-plugins enable --offline rabbitmq_consistent_hash_exchange && \
    rm -rf /tmp/dmx3.7.zip
