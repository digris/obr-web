import mitt from "mitt";

const eventBus = mitt();

eventBus.on("*", (type, e) => console.log(type, e));

// @ts-ignore
window.eventBus = eventBus;

export default eventBus;
