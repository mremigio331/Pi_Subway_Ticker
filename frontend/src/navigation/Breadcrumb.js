import { BreadcrumbGroup } from '@cloudscape-design/components/';
import { useNavigate } from 'react-router-dom';

const TickerBreadcrumb = () => {
    const navigate = useNavigate();

    const handleFollow = (event) => {
        event.preventDefault();
        navigate(event.detail.href);
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
