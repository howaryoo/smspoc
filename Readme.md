# Prerequisites

## production requirements

 * requirements.txt
 
## test requirements

 * test-requirements.txt
 
# Proposed implementation

 * Non blocking using asyncio
 * restful API with [swagger UI provided](http://localhost:5000/docs?url=http://localhost:5000/static/schema.yml)
 
# Usage

## Run tests
    ~/projects/se⟫ make test

## Run the server
    ~/projects/se⟫ make run
        
# Limitations

 * Memory hungry
 * Actual index and search functions are blocking
