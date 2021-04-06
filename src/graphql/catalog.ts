import gql from 'graphql-tag';
import apolloClient from './client';

async function getMedia(limit: number, offset: number) {
  const query = gql`
  {
    media(first: ${limit} offset: ${offset}) {
      edges {
        # cursor,
        node {
          id,
          name,
          uid,
          duration,
          artistDisplay
        }
      }
    }
  }`;
  const result = await apolloClient.query({ query });
  const media = result.data.media.edges.map((n: any) => n.node);
  const response = {
    data: {
      results: media,
      // results: [
      //   { name: 'the name 1' },
      //   { name: 'the name 2' },
      // ],
    },
  };
  return response.data;
}

// eslint-disable-next-line import/prefer-default-export
export { getMedia };
