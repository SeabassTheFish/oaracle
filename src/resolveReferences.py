#!usr/bin/local/python3
import json

def resolveRefs(jsons):
    if (type(jsons) == 'string'):
        jsonOutput = json.loads(jsons)

    byid = {}, # all objects by id
    refs = []; # references to objects that could not be resolved
    def json(obj, prop, parent) {
        if (type(obj) != 'object' or !obj): # a primitive value
            return obj;
        if (type(obj) === '[object Array]'):
            for i in range(len(obj)):
                # check also if the array element is not a primitive value
                if (type(obj[i]) != 'object' or !obj[i]): // a primitive value
                    continue;
                elif ("$ref" in obj[i]):
                    obj[i] = recurse(obj[i], i, obj);
                else
                    obj[i] = recurse(obj[i], prop, obj);
            return obj;
        }
        if ("$ref" in obj) { // a reference
            var ref = obj.$ref;
            if (ref in byid)
                return byid[ref];
            // else we have to make it lazy:
            refs.push([parent, prop, ref]);
            return;
        } else if ("$id" in obj) {
            var id = obj.$id;
            delete obj.$id;
            if ("$values" in obj) // an array
                obj = obj.$values.map(recurse);
            else // a plain object
                for (var prop in obj)
                    obj[prop] = recurse(obj[prop], prop, obj);
            byid[id] = obj;
        }
        return obj;
    })(json); // run it!

    for (var i = 0; i < refs.length; i++) { // resolve previously unknown references
        var ref = refs[i];
        ref[0][ref[1]] = byid[ref[2]];
        // Notice that this throws if you put in a reference at top-level
    }
    print(json);
