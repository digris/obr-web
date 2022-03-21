const parseFilterQuery = (query: any) => {
  let tags = query?.tags ?? [];
  // const q = query?.q ?? null;
  if (typeof (tags) === 'string' || tags instanceof String) {
    tags = [tags];
  }
  const filter = {
    ...query,
    tags,
    // q,
  };
  return filter;
};

export { parseFilterQuery };
