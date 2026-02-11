
const url = 'api';



const data = {
    "name": "",
    "email": "",
    "phone": "",
    "documnts": "",
    "national_id": ""
};

async function sendTraineeData() {
    try {
        const response = await fetch(url, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(data)
        });

        if (!response.ok) {
            throw new Error(`error${response.status}`);
        }

        const result = await response.json();
        console.log('done!', result);


    } catch (error) {
        console.error('error', error);
    }
}


sendTraineeData();