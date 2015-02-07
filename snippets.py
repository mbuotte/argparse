import sys
import logging
import argparse
import psycopg2


# Set the log output file, and the log level
logging.basicConfig(filename="snippets.log", level=logging.DEBUG)

def put(name, snippet):
    """Store a snippet with an associated name."""
    logging.debug("Connecting to PostgreSQL")
    connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
    logging.debug("Database connection established.")


    logging.info("Storing snippet {!r}: {!r}".format(name, snippet))
    cursor = connection.cursor()
    try:
      command = "insert into snippets values (%s, %s)"
      cursor.execute(command, (name, snippet))
    except psycopg2.IntegrityError as e:
      connection.rollback()
      command = "update snippets set message=%s where keyword=%s"
      cursor.execute(command,(snippet,name))
    connection.commit()
    logging.debug("Snippet stored successfully.")
    return name, snippet
  
  
def get(name):
    """Retrieve the snippet with a given name.
    If there is no such snippet return a -1 indicating snippet not found
    Returns the snippet.
    """
    logging.debug("Connecting to PostgreSQL")
    connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
    logging.debug("Database connection established.")

    logging.info("Retrieving snippet {!r}".format(name))

    with connection, connection.cursor() as cursor:
        cursor.execute("select * from snippets where keyword=%s", (name,))
        record = cursor.fetchone()
   
    if not record:
      logging.debug("No snippet was retrieved for {!r}".format(name))
      # No snippet was found
    else:
      logging.debug("Snippet retrieved as {!r}".format(record[1]))
      return record[1]

   
def main():
    """Main function"""
    logging.info("Constructing parser")

    parser = argparse.ArgumentParser(description="Store and retrieve snippets of text")
    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # Subparser for the put command
    logging.debug("Constructing put subparser")
    put_parser = subparsers.add_parser("put", help="Store a snippet")
    put_parser.add_argument("name", help="The name of the snippet")
    put_parser.add_argument("snippet", help="The snippet text")
    
        # Subparser for the put command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve snippet of text")
    get_parser.add_argument("name", help="The name of the snippet")
   
    arguments = parser.parse_args(sys.argv[1:])
    # Convert parsed arguments from Namespace to dictionary
    arguments = vars(arguments)
    command = arguments.pop("command")

    if command == "put":
        name, snippet = put(**arguments)
        print("Stored {!r} as {!r}".format(snippet, name))
    elif command == "get":
        snippet = get(**arguments)
        print("Retrieved snippet: {!r}".format(snippet))    
    
    
if __name__ == "__main__":
    main()