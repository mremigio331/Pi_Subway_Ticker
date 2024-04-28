import { TrainLogos } from '../../utility/SubwayLogos';

export const getRandomTrainLogos = () => {
    const numLogosToSelect = 14;
    const selectedLogos = [];

    const trainNames = Object.keys(TrainLogos);

    const randomIndices = [];
    while (randomIndices.length < numLogosToSelect) {
        const randomIndex = Math.floor(Math.random() * trainNames.length);
        if (!randomIndices.includes(randomIndex)) {
            randomIndices.push(randomIndex);
        }
    }

    randomIndices.forEach((index) => {
        const trainName = trainNames[index];
        selectedLogos.push(TrainLogos[trainName]);
    });

    return selectedLogos;
};
