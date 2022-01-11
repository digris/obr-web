// @ts-ignore
const { settings } = document;

const userSettings = { ...settings };

// NOTE: implement language / locale detection
userSettings.API_BASE_URL = `${userSettings.API_BASE_URL}`;

// console.dir(userSettings);

export default userSettings;
