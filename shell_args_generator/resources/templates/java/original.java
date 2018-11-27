package com.epam.fiodarau.kafka.clutils;


import org.apache.commons.cli.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * class for managing by command line arguments
 */
public class CommandLineManager {
    private static final Logger LOGGER = LoggerFactory.getLogger(CommandLineManager.class);

    private Option helpOption;

    private Option userOption;
    private Option hotelOption;
    private Option maxBookingOption;
    private Option maxUserOption;
    private Option maxHotelOption;
    private Option topicOption;
    private Option serverOption;
    private Option threadsOption;
    private Options options;

    private String userFile;
    private String hotelFile;
    private Integer maxBooking;
    private Integer maxUser;
    private Integer maxHotel;
    private String topic;
    private String server;
    private Integer threads;
    private boolean needHelp;


    /**
     * KafkaProducer manager with current command line's args
     *
     * @param args command line's arguments
     * @throws ParseException throws when options are was not valid
     */
    public CommandLineManager(String[] args) throws ParseException {
        options = new Options();

        helpOption = new Option("h", "help", false, "print help");

        userOption = new Option("ug", "usergenlist", true, "input user gener file");
        hotelOption = new Option("hg", "hotelgenlist", true, "input hotel gener file");
        maxBookingOption = new Option("mb", "maxbooking", true, "max booking");
        maxUserOption = new Option("mu", "maxuser", true, "max user");
        maxHotelOption = new Option("mh", "maxhotel", true, "max hotel");
        topicOption = new Option("t", "topic", true, "set topic");
        serverOption = new Option("s", "server", true, "set server");
        threadsOption = new Option("th", "threads", true, "set threads");


        userOption.setArgs(1);
        userOption.setOptionalArg(false);
        userOption.setArgName("input user gener file");

        hotelOption.setArgs(1);
        hotelOption.setOptionalArg(false);
        hotelOption.setArgName("input hotel gener file");

        maxBookingOption.setArgs(1);
        maxBookingOption.setOptionalArg(false);
        maxBookingOption.setArgName("max booking");

        maxUserOption.setArgs(1);
        maxUserOption.setOptionalArg(false);
        maxUserOption.setArgName("max user");

        maxHotelOption.setArgs(1);
        maxHotelOption.setOptionalArg(false);
        maxHotelOption.setArgName("max hotel");

        topicOption.setArgs(1);
        topicOption.setOptionalArg(false);
        topicOption.setArgName("topic name");

        serverOption.setArgs(1);
        serverOption.setOptionalArg(false);
        serverOption.setArgName("kafka server");

        threadsOption.setArgs(1);
        threadsOption.setOptionalArg(false);
        threadsOption.setArgName("count of threads");

        options.addOption(helpOption);
        options.addOption(userOption);
        options.addOption(hotelOption);
        options.addOption(maxBookingOption);
        options.addOption(maxUserOption);
        options.addOption(maxHotelOption);
        options.addOption(topicOption);
        options.addOption(serverOption);
        options.addOption(threadsOption);

        parse(args);
    }

    /**
     * parse command line's arguments
     *
     * @param args command line's arguments
     * @throws ParseException throws when options are was not valid
     */
    private void parse(String[] args) throws ParseException {
        CommandLineParser parser = new DefaultParser();
        CommandLine commandLine = parser.parse(options, args);
        needHelp = commandLine.hasOption(helpOption.getLongOpt());

        if (!needHelp) {
            if (!commandLine.hasOption(userOption.getLongOpt())) {
                throw new MissingArgumentException("user file param was missed");
            }
            LOGGER.debug("find user option \"" + commandLine.getOptionValue(userOption.getLongOpt()) + "\"");

            if (!commandLine.hasOption(hotelOption.getLongOpt())) {
                throw new MissingArgumentException("hotel file param was missed");
            }
            LOGGER.debug("find hotel option \"" + commandLine.getOptionValue(hotelOption.getLongOpt()) + "\"");

            if (!commandLine.hasOption(maxBookingOption.getLongOpt())) {
                throw new MissingArgumentException("max booking param was missed");
            }
            LOGGER.debug("max booking option \"" + commandLine.getOptionValue(maxBookingOption.getLongOpt()) + "\"");

            if (!commandLine.hasOption(maxUserOption.getLongOpt())) {
                throw new MissingArgumentException("max user param was missed");
            }
            LOGGER.debug("max user option \"" + commandLine.getOptionValue(maxUserOption.getLongOpt()) + "\"");

            if (!commandLine.hasOption(maxHotelOption.getLongOpt())) {
                throw new MissingArgumentException("max hotel param was missed");
            }
            LOGGER.debug("max hotel option \"" + commandLine.getOptionValue(maxHotelOption.getLongOpt()) + "\"");

            if (!commandLine.hasOption(topicOption.getLongOpt())) {
                throw new MissingArgumentException("topic param was missed");
            }
            LOGGER.debug("topic option \"" + commandLine.getOptionValue(topicOption.getLongOpt()) + "\"");

            if (!commandLine.hasOption(serverOption.getLongOpt())) {
                throw new MissingArgumentException("server param was missed");
            }
            LOGGER.debug("server option \"" + commandLine.getOptionValue(serverOption.getLongOpt()) + "\"");

            if (!commandLine.hasOption(threadsOption.getLongOpt())) {
                throw new MissingArgumentException("threads param was missed");
            }
            LOGGER.debug("threads option \"" + commandLine.getOptionValue(threadsOption.getLongOpt()) + "\"");

            userFile = commandLine.getOptionValue(userOption.getLongOpt());
            hotelFile = commandLine.getOptionValue(hotelOption.getLongOpt());
            maxBooking = Integer.valueOf(commandLine.getOptionValue(maxBookingOption.getLongOpt()));
            maxUser = Integer.valueOf(commandLine.getOptionValue(maxUserOption.getLongOpt()));
            maxHotel = Integer.valueOf(commandLine.getOptionValue(maxHotelOption.getLongOpt()));
            topic = commandLine.getOptionValue(topicOption.getLongOpt());
            server = commandLine.getOptionValue(serverOption.getLongOpt());
            threads = Integer.valueOf(commandLine.getOptionValue(threadsOption.getLongOpt()));
        }
    }

    /**
     * getting file with user genlist
     *
     * @return path to user genlist
     */
    public String getUserFile() {
        return userFile;
    }

    /**
     * getting file with hotel
     *
     * @return path to file with hotel genlist
     */
    public String getHotelFile() {
        return hotelFile;
    }

    /**
     * getting max count of generate booking flags (booked/unbooked)
     *
     * @return max count of generate booking flags
     */
    public Integer getMaxBooking() {
        return maxBooking;
    }

    /**
     * getting max count user of generate user id from user genlist
     *
     * @return max count of generate user id
     */
    public Integer getMaxUser() {
        return maxUser;
    }

    /**
     * getting max count hotel of generate hotel (hotel_continent, hotel_country, hotel_market) from hotel genlist
     *
     * @return max count of generate hotel
     */
    public Integer getMaxHotel() {
        return maxHotel;
    }

    /**
     * getting kafka topic name
     *
     * @return kafka topic name
     */
    public String getTopic() {
        return topic;
    }

    /**
     * getting kafka server address
     *
     * @return kafka server address
     */
    public String getServer() {
        return server;
    }

    /**
     * getting threads count
     *
     * @return threads count
     */
    public Integer getThreads() {
        return threads;
    }

    /**
     * getting help flag from parsed commandline
     *
     * @return help flag from parsed commanline
     */
    public boolean isNeedHelp() {
        return needHelp;
    }

    /**
     * print help message
     */
    public void printHelp() {
        HelpFormatter formatter = new HelpFormatter();
        String syntax = "csvSerializer";
        String usageHeader = "Tool for serialize data from csv file";
        String usageFooter = "<Aliaksei_fiodarau@epam.com> 05.10.2018";
        System.out.println("\n===============================================");
        System.out.println("                     HELP");
        System.out.println("===============================================");
        formatter.printHelp(syntax, usageHeader, options, usageFooter);
    }
}
