var timerElement = document.getElementById('timer');
var rollButton = document.getElementById('roll-btn');
var keepButton = document.getElementById('keep-btn');
var passButton = document.getElementById('pass-btn');

function startTimer(timeLeftInSeconds) {
    var timer = setInterval(function() {
        timeLeftInSeconds--;
        var minutes = Math.floor(timeLeftInSeconds / 60);
        var seconds = timeLeftInSeconds % 60;
        timerElement.innerHTML = 'Countdown to next roll: ' + minutes + 'm ' + seconds + 's';

        if (timeLeftInSeconds <= 0) {
            clearInterval(timer);
            rollButton.style.display = 'block';
            keepButton.style.display = 'none';
            passButton.style.display = 'none';
            timerElement.innerHTML = '';
        }
    }, 1000);
}
document.getElementById('roll-btn').addEventListener('click', function() {
    fetch('/roll-api/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
        },
        body: JSON.stringify({
            endpoints: [
                'https://swapi.dev/api/people/',
                'https://swapi.dev/api/starships/',
                'https://swapi.dev/api/planets/'
            ]
        })
    })
    .then(response => response.json())
    .then(data => {
        console.log(data);
        if (data.results) {
            // Access the randomly selected results here
            console.log(data.results);
            
            const items = data.results;
            const peopleContainer = document.querySelector(".people-container");
            const starshipContainer = document.querySelector(".starship-container");
            const planetContainer = document.querySelector(".planet-container");
            
            // Clear existing content from containers
            if (peopleContainer) {
                peopleContainer.innerHTML = '';
            }
            if (starshipContainer) {
                starshipContainer.innerHTML = '';
            }
            if (planetContainer) {
                planetContainer.innerHTML = '';
            }
            
            items.forEach(item => {
                const itemDiv = document.createElement("div");
                itemDiv.classList.add(item.type);
                
                const itemCategory = document.createElement("p");
                itemCategory.textContent = "Category: " + item.type;  // Add category element
                itemDiv.appendChild(itemCategory);

                const itemName = document.createElement("p");
                itemName.textContent = 'Name:' + item.name;
                itemDiv.appendChild(itemName);
                
                
                if (item.type === "people") {
                    const itemHairColor = document.createElement("p");
                    itemHairColor.textContent = "Hair color: " + item.hair_color;
                    itemDiv.appendChild(itemHairColor);
                
                    const itemGender = document.createElement("p");
                    itemGender.textContent = "Gender: " + item.gender;
                    itemDiv.appendChild(itemGender);
                
                    if (peopleContainer) {
                        peopleContainer.appendChild(itemDiv);
                    }
                } else if (item.type === "starship") {
                    const itemManufacturer = document.createElement("p");
                    itemManufacturer.textContent = "Manufacturer: " + item.manufacturer;
                    itemDiv.appendChild(itemManufacturer);
                
                    const itemModel = document.createElement("p");
                    itemModel.textContent = "Model: " + item.model;
                    itemDiv.appendChild(itemModel);
                
                    if (starshipContainer) {
                        starshipContainer.appendChild(itemDiv);
                    }
                } else if (item.type === "planet") {
                    const itemPopulation = document.createElement("p");
                    itemPopulation.textContent = "Population: " + item.population;
                    itemDiv.appendChild(itemPopulation);
                
                    const itemTerrain = document.createElement("p");
                    itemTerrain.textContent = "Terrain: " + item.terrain;
                    itemDiv.appendChild(itemTerrain);
                
                    if (planetContainer) {
                        planetContainer.appendChild(itemDiv);
                    }
                }
                startTimer(60);
            });

                // Show the "Keep" and "Pass" buttons
                document.getElementById('roll-btn').style.display = 'none';
                document.getElementById('keep-btn').style.display = 'block';
                document.getElementById('pass-btn').style.display = 'block';
            
                // Add event listener to "Keep" button
                document.getElementById('keep-btn').addEventListener('click', function() {
                    // Store the items in the database
                    fetch('/store-items/', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json',
                            'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                        },
                        body: JSON.stringify(data),
                    })
                    .then(response => response.json())
                    .then(data => {
                        console.log(data);
                        document.getElementById('result').innerHTML = 'Excellent choice, padawan.';
                        document.getElementById('keep-btn').style.display = 'none';
                        document.getElementById('pass-btn').style.display = 'none';
                        document.getElementById('roll-btn').style.display = 'block';
                    })
                    .catch(error => console.log(error));
                });
                document.getElementById('pass-btn').addEventListener('click', function() {
                    // Reset to "roll" state
                    const peopleContainer = document.querySelector(".people-container");
                    const starshipContainer = document.querySelector(".starship-container");
                    const planetContainer = document.querySelector(".planet-container");
                    if (peopleContainer) {
                        peopleContainer.innerHTML = '';
                    }
                    if (starshipContainer) {
                        starshipContainer.innerHTML = '';
                    }
                    if (planetContainer) {
                        planetContainer.innerHTML = '';
                    }
                    document.getElementById('keep-btn').style.display = 'none';
                    document.getElementById('pass-btn').style.display = 'none';
                    document.getElementById('roll-btn').style.display = 'block';
                });
            }
        });
    });
