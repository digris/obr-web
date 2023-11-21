const playlistTitle = (playlist: any) => {
  // @ts-ignore
  const name = playlist.series ? playlist.series.name : playlist.name;
  // @ts-ignore
  const appendix = playlist.series ? playlist.series.episode : null;

  if (name && appendix) {
    return `${name} #${appendix}`;
  }
  return name;
};

export { playlistTitle };
