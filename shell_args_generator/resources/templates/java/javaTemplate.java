import org.apache.commons.cli.*;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

/**
 * class for managing by command line arguments
 */
public class CommandLineManager {
    private static final Logger LOGGER = LoggerFactory.getLogger(CommandLineManager.class);

    private Options options;
    
    %OPTIONS%

    %PARAMETERS%


    /**
     * %TITLE% manager with current command line's args
     *
     * @param args command line's arguments
     * @throws ParseException throws when options are was not valid
     */
    public CommandLineManager(String[] args) throws ParseException {
        options = new Options();

        %CREATE_OPTIONS%

        %SET_ARGUMENTS%

        %ADD_OPTIONS%

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
            %CHECK_OPTIONS%
            %SET_OPTIONS%
        }
    }

    %OPTIONS_GETTERS%

    /**
     * print help message
     */
    public void printHelp() {
        HelpFormatter formatter = new HelpFormatter();
        String syntax = "%TITLE%";
        String usageHeader = "%DESCRIPTION%";
        String usageFooter = "%AUTHOR% %VERSION%";
        System.out.println("\n===============================================");
        System.out.println("                     HELP");
        System.out.println("===============================================");
        formatter.printHelp(syntax, usageHeader, options, usageFooter);
    }
}
