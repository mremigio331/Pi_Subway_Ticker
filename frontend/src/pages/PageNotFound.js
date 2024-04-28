import React from 'react';
import { Box, Container, ContentLayout, Header, SpaceBetween } from '@cloudscape-design/components';
import { Link } from 'react-router-dom';

const NotFoundPage = () => {
    return (
        <ContentLayout header={<Header variant="h1">??????????</Header>}>
            <Container header={<Header variant="h1">Looks Like You're Lost</Header>}>
                How did you end up here? I have no clue where you are, may want to go back home.
            </Container>
        </ContentLayout>
    );
};

export default NotFoundPage;
