const parseFilterQuery = (query: any) => {
  let tags = query?.tags ?? [];
  const q = query?.q ?? null;
  if (typeof (tags) === 'string') {
    tags = [tags];
  }
  const filter = {
    tags,
    q,
  };
  return filter;
};

export { parseFilterQuery };
