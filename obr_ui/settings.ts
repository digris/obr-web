// @ts-ignore
const { settings } = document;

const userSettings = { ...settings };

userSettings.locale = "de";

// NOTE: implement language / locale detection
userSettings.API_BASE_URL = `${userSettings.API_BASE_URL}`;

// console.dir(userSettings);

export default userSettings;
