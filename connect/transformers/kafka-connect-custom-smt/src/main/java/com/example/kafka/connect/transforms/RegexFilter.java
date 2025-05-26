package com.example.kafka.connect.transforms;

import org.apache.kafka.common.config.ConfigDef;
import org.apache.kafka.connect.connector.ConnectRecord;
import org.apache.kafka.connect.transforms.Transformation;

import java.util.Map;
import java.util.regex.Pattern;

public class RegexFilter<R extends ConnectRecord<R>> implements Transformation<R> {

    public static final String REGEX_CONFIG = "regex";
    private Pattern pattern;

    @Override
    public R apply(R record) {
        if (record.value() != null && pattern.matcher(record.value().toString()).find()) {
            return record; // Keep the record if it matches the regex
        }
        return null; // Filter out the record if it doesn't match
    }

    @Override
    public ConfigDef config() {
        return new ConfigDef()
                .define(REGEX_CONFIG, ConfigDef.Type.STRING, ConfigDef.Importance.HIGH, "Regex to filter records");
    }

    @Override
    public void configure(Map<String, ?> configs) {
        String regex = (String) configs.get(REGEX_CONFIG);
        pattern = Pattern.compile(regex);
    }

    @Override
    public void close() {
        // No resources to close
    }
}