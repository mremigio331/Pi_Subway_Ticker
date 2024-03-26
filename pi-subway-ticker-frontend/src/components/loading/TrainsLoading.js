import { TrainLogos } from '../current-subway-info/SubwayLogos';

export const getRandomTrainLogos = () => {
    const numLogosToSelect = 10;
    const selectedLogos = [];

    const trainNames = Object.keys(TrainLogos);

    // Generate 10 unique random indices
    const randomIndices = [];
    while (randomIndices.length < numLogosToSelect) {
        const randomIndex = Math.floor(Math.random() * trainNames.length);
        if (!randomIndices.includes(randomIndex)) {
            randomIndices.push(randomIndex);
        }
    }

    // Push the corresponding logos to the selectedLogos array
    randomIndices.forEach((index) => {
        const trainName = trainNames[index];
        selectedLogos.push(TrainLogos[trainName]);
    });

    return selectedLogos;
};
