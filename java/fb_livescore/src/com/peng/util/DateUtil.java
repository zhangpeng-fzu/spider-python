package com.peng.util;

import java.text.SimpleDateFormat;

public class DateUtil {
    static SimpleDateFormat dateFormat = new SimpleDateFormat("yyyy-MM-dd");

    public static SimpleDateFormat getDateFormat() {
        return dateFormat;
    }
}
