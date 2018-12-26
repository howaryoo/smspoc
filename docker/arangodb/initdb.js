const rawdb = process.env.ARANGO_INIT_DB
const dbs = rawdb.split(";")

const raw_collections = process.env.ARANGO_INIT_COLLECTIONS
const colls = raw_collections.split(";")


for (var i in dbs) {
    db._createDatabase(dbs[i]);
    db._useDatabase(dbs[i]);

    for (var i in colls) {
        db._create(colls[i]);
    }
}


