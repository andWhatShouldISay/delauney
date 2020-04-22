key='пиво'

cities=[
   'New York',
   'Los Angeles',
   'Chicago',
   'Houston',
   'Phoenix',
   'Philadelphia',
   'San Antonio',
   'San Diego',
   'Dallas',
   'San Jose',
   'Austin',
   'Jacksonville',
   'Fort Worth',
   'Columbus',
   'San Francisco',
   'Charlotte',
   'Indianapolis',
   'Seattle',
   'Denver',
   'Washington',
   'Boston',
   'Detroit',
   'Nashville',
   'Portland',
   'Memphis',
   'Oklahoma City',
   'Las Vegas',
   'Louisville',
   'Baltimore',
   'Milwaukee',
   'Tucson',
   'Fresno',
   'Mesa',
   'Sacramento',
   'Atlanta',
   'Kansas City',
   'Colorado Springs',
   'Miami',
   'Raleigh',
   'Omaha',
   'Long Beach',
   'Virginia Beach',
   'Oakland',
   'Minneapolis',
   'Tulsa',
   'Arlington',
   'Tampa',
   'New Orleans',
   'Wichita',
   'Cleveland',
   'Bakersfield',
   'Anaheim',
   'Santa Ana',
   'Riverside',
   'Corpus Christi',
   'Lexington',
   'Stockton',
   'Henderson',
   'Saint Paul',
   'St. Louis',
   'Cincinnati',
   'Pittsburgh',
   'Greensboro',
   'Plano',
   'Lincoln Nebraska',
   'Orlando',
   'Irvine',
   'Newark',
   'Toledo',
   'Durham',
   'Chula Vista',
   'Fort Wayne',
   'Jersey City',
   'St. Petersburg',
   'Laredo',
   'Madison',
   'Chandler',
   'Buffalo',
   'Lubbock',
   'Scottsdale',
   'Reno',
   'Glendale',
   'Gilbert',
   'Winston–Salem',
   'North Las Vegas',
   'Norfolk',
   'Chesapeake',
   'Garland',
   'Irving',
   'Hialeah',
   'Fremont',
   'Boise',
   'Richmond',
   'Baton Rouge',
   'Spokane',
   'Santa Fe',
   'Flagstaff',
   'Castle Rock',
   'Cheyenne',
   'Parker',
   'Centennial',
   'Lakewood',
   'Arvada',
   'Aurora',
   'Westminster',
   'Thornton',
   'Broomfield',
   'Boulder',
   'Albuquerque',
   'Rio Rancho',
   'Commerce City',
   'Casper',
   'Fort Collins',
   'Longmont',
   'Loveland',
   'Carson City',
   'Orem',
   'Idaho Falls',
   'Pueblo',
   'Greeley',
   'Grand Junction',
   'Provo',
   'Logan',
   'Pocatello',
   'Sparks',
   'West Jordan',
   'West Valley City',
   'Salt Lake City',
   'Las Cruces',
   'El Paso',
   'Bend',
   'Amarillo',
   'Great Falls',

   'Montgomery',
   'Des Moines',
   'Little Rock',
   'Tallahassee',
   'Providence',
   'Jackson',
   'Salem',
   'Columbia',
   'Topeka',
   'Hartford',
   'Springfield',
   'Lansing',
   'Albany',
   'Trenton',
   'Bismarck',
   'Cheyenne',
   'Carson City',
   'Charleston',
   'Harrisburg',
   'Olympia',
   'Jefferson City',
   'Concord',
   'Annapolis',
   'Dover',
   'Helena',
   'Frankfort',
   'Augusta',
   'Pierre',
   'Montpelier',
]
const https = require('https');


var E={}
var G={}

go(0)

function addr(city){
    var c2=city.replace(' ','%20')+"%20US"
    c2=c2.replace('.','%2E')
    c2=c2.replace('–','%2D')
    var a='https://maps.googleapis.com/maps/api/geocode/json?address='+c2+'&key='+key
    return a
}

function go(X){
    if (X==cities.length)
    {
        ready()
        return
    }
    for (var i=X;i<=X;i++){
        G[cities[i]]=1
        var c=cities[i]
        a=addr(cities[i])

        https.get(a, (resp) => {
            let data = '';

            // A chunk of data has been recieved.
            resp.on('data', (chunk) => {
                data += chunk
            });

             // The whole response has been received. Print out the result.
            resp.on('end', () => {
                var obj=JSON.parse(data)

                if (obj.results[0]==undefined)
                    console.log(obj)

                var x=obj.results[0].geometry.location.lat
                var y=obj.results[0].geometry.location.lng
                var name=obj.results[0].address_components[0].long_name
                if (name.indexOf('1')!=-1){
                    console.log(obj)
                    console.log(c)
                }

                var a2='https://maps.googleapis.com/maps/api/elevation/json?locations='+x+','+y+'&key='+key
                https.get(a2, (resp) => {
                    let data = '';

                    // A chunk of data has been recieved.
                    resp.on('data', (chunk) => {
                        data += chunk
                    });

                     // The whole response has been received. Print out the result.
                    resp.on('end', () => {
                        var obj=JSON.parse(data)
                        if (obj.results[0]!=undefined){
                            E[name]={lat:x,lng:y,elev:obj.results[0].elevation}
                            console.log(name)
                            if (G[name]==undefined)
                                G[name]=0;
                            G[name]-=1
                        }
                        else
                            console.log(name,obj)
                        go(X+1)
                    });

                }).on("error", (err) => {
                    console.log("Error: " + err.message);
                });

            });

        }).on("error", (err) => {
            console.log("Error: " + err.message);
        });
    }
}


function ready(){
    for (k in G){
        if (G[k]!==0){
            console.log(k,G[k])
            if (G[k]==-1){
                console.log(E[k])
            }
        }
    }
    console.log(E)
    console.log(JSON.stringify(E))
}