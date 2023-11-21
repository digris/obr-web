const zeroPad = (n: number) => {
  return n > 9 ? `${n}` : `0${n}`;
};

export { zeroPad };
