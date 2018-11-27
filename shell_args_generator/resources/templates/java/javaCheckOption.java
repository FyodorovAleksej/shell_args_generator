if (!commandLine.hasOption(%OPTION_NAME%.getLongOpt())) {
    throw new MissingArgumentException("%OPTION_DESCRIPTION% param was missed");
}
LOGGER.debug("find %OPTION_NAME% \"" + commandLine.getOptionValue(%OPTION_NAME%.getLongOpt()) + "\"");
