import sys
import logging
import argparse
import psycopg2
import pprint


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
    
def catalog():
    """Return all snippet names
    """
    logging.debug("Connecting to PostgreSQL")
    connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
    logging.debug("Database connection established.")

    logging.info("Retrieving snippet names")

    with connection, connection.cursor() as cursor:
        cursor.execute("select keyword from snippets")
        records = cursor.fetchall()
   
    if not records:
      logging.debug("No records returned")
      # No snippet was found
    else:
      logging.debug("Records Returned")
      pprint.pprint(records)
      return (1)

def search(name):
    """Retrieve the snippet name like the given name.
    If there is no such snippet return a -1 indicating snippet not found
    Returns the snippet name.
    """
    logging.debug("Connecting to PostgreSQL")
    connection = psycopg2.connect("dbname='snippets' user='action' host='localhost'")
    logging.debug("Database connection established.")

    logging.info("Looking for snippet name like {!r}".format(name))

    with connection, connection.cursor() as cursor:
        lookfor = '%' + name + '%'
        cursor.execute("select keyword from snippets where keyword like %s", (lookfor,))
        record = cursor.fetchone()
   
    if not record:
      logging.debug("No snippet name exists like {!r}".format(name))
      # No snippet name was found
    else:
      logging.debug("Snippet name retrieved as {!r}".format(record))
      return record
   
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
    
    # Subparser for the get command
    logging.debug("Constructing get subparser")
    get_parser = subparsers.add_parser("get", help="Retrieve snippet of text")
    get_parser.add_argument("name", help="The name of the snippet")
   
      # Subparser for the catalog command

    # Subparser for the catalog command
    logging.debug("Constructing catalog subparser")
    catalog_parser = subparsers.add_parser("catalog", help="Show all snippet names")

    # Subparser for the searcg command
    logging.debug("Constructing search subparser")
    search_parser = subparsers.add_parser("search", help="Retrieve snippet of text")
    search_parser.add_argument("name", help="The name of the snippet")
   
    
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
    elif command == "catalog":
        count = catalog()
        print ("Listed all snippet names")
    elif command == "search":
        name = search(**arguments)
        print("Retrieved name: {!r}".format(name))
    
    
if __name__ == "__main__":
    main()