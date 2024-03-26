import { BreadcrumbGroup } from '@cloudscape-design/components/';
import { useNavigate } from 'react-router-dom';

const TickerBreadcrumb = () => {
    const navigate = useNavigate(); // Use navigate hook from react-router-dom

    const handleFollow = (event) => {
        event.preventDefault();
        navigate(event.detail.href); // Use navigate to handle navigation
    };

    return (
        <BreadcrumbGroup
            items={[
                { text: 'Home', href: '/' },
                { text: 'General Settings', href: '/settings' },
            ]}
            ariaLabel="Breadcrumbs"
            onFollow={handleFollow}
        />
    );
};

export default TickerBreadcrumb;
